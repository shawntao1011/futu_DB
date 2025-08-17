import logging
import queue
import threading, time
from dataclasses import dataclass
from typing import Literal, Callable, Tuple, Type

logger = logging.getLogger(__name__)

DropPolicy = Literal["drop_oldest", "drop_newest", "block"]

@dataclass
class SinkConfig:
    name: str
    publish_fn: Callable[[str, any], None]
    connect_fn: Callable[[str, any], None] | None
    is_ready_fn: Callable[[str, any], bool] | None
    close_fn: Callable[[str, any], None] | None

    max_queue: int = 10000
    retry_times: int = 1
    retry_backoff_s: float = 0.05

    reconnect_initial_s: float = 0.5
    reconnect_max_s: float = 0.5
    recoverable: Tuple[Type[BaseException], ...] = (ConnectionError, TimeoutError, BrokenPipeError, OSError)

    requeue_on_failure: bool = False

@dataclass
class _SinkState:
    q: "queue.Queue[Tuple[str, any]]"
    t: threading.Thread
    connected: bool = False
    backoff_s: float = 0.0
    enq: int = 0
    sent: int = 0
    dropped: int = 0
    errors: int = 0
    last_err: str | None = None

class FanoutPublisher:
    """
    线程化扇出发布器（强隔离 + 迟连可用）
      - 每个下游独立队列+工作线程，互不影响
      - 懒连接：未连上时不阻塞启动；按指数退避自动重连
      - 发布失败：可配置重试 / 是否回插队列；遇 recoverable 异常会触发重连
      - 背压策略：drop_oldest / drop_newest / block
    """
    def __init__(self, sinks: list[SinkConfig], drop_policy: DropPolicy = "drop_oldest"):
        self._cfgs: dict[str, SinkConfig] = { s.name: s for s in sinks }
        self._states: dict[str, _SinkState] = {}
        self._drop_policy: DropPolicy = drop_policy
        self._stop = threading.Event()
        self._start_workers()


    def publish(self, table: str, data: any) -> None:
        for name, st in self._states.items():
            q = st.q
            try:
                if self._drop_policy == "drop_oldest" and q.full():
                    try:
                        q.get_nowait()
                        st.dropped += 1
                        q.task_done()
                    except queue.Empty:
                        pass
                if self._drop_policy == "drop_newest" and q.full():
                    st.dropped += 1
                    continue
                q.put_nowait((table, data))
                st.enq += 1
            except queue.Full:
                st.dropped += 1
                logger.warning("sink %s queue full; dropped one", name)

    def close(self, wait: bool = True, timeout: float | None = 5.0) -> None:
        self._stop.set()
        for st in self._states.values():
            try: st.q.put_nowait((None, None))  # sentinel
            except Exception: pass
        if wait:
            start = time.time()
            for st in self._states.values():
                st.q.join()
            for st in self._states.values():
                remain = None if timeout is None else max(0.0, timeout - (time.time()-start))
                st.t.join(remain)
        # 调用各自 close_fn
        for name, cfg in self._cfgs.items():
            if cfg.close_fn:
                try: cfg.close_fn()
                except Exception: logger.exception("sink %s close_fn raised", name)

    def counters(self) -> dict[str, dict[str, any]]:
        return {
            name: dict(
                queued=st.q.qsize(), enq=st.enq, sent=st.sent,
                dropped=st.dropped, errors=st.errors, connected=st.connected,
                last_err=st.last_err, backoff_s=st.backoff_s
            )
            for name, st in self._states.items()
        }


    # ---------- internals ----------
    def _start_workers(self):
        for name, cfg in self._cfgs.items():
            q: "queue.Queue[Tuple[str, any]]" = queue.Queue(maxsize=cfg.max_queue)
            t = threading.Thread(target=self._worker, args=(name,), name=f"fanout-{name}", daemon=True)
            self._states[name] = _SinkState(q=q, t=t, connected=False, backoff_s=cfg.reconnect_initial_s)
            t.start()

    def _ensure_connected(self, name: str, cfg: SinkConfig, st: _SinkState) -> bool:
        if self._stop.is_set():
            return False
        # 没定义 connect_fn / is_ready_fn：视为总是已连
        if cfg.connect_fn is None and cfg.is_ready_fn is None:
            st.connected = True
            return True
        # 已连且 ready_fn 也 ok
        if st.connected and (cfg.is_ready_fn is None or self._safe_is_ready(cfg, st)):
            return True
        # 重连流程（指数退避）
        while not self._stop.is_set():
            try:
                if cfg.connect_fn:
                    cfg.connect_fn()
                if cfg.is_ready_fn is None or self._safe_is_ready(cfg, st):
                    st.connected = True
                    st.backoff_s = cfg.reconnect_initial_s
                    return True
            except Exception as e:
                st.connected = False
                st.last_err = f"connect: {e!r}"
                logger.warning("sink %s connect failed: %r; retry in %.2fs", name, e, st.backoff_s)
            time.sleep(st.backoff_s)
            st.backoff_s = min(cfg.reconnect_max_s, max(cfg.reconnect_initial_s, st.backoff_s * 2))
        return False

    def _safe_is_ready(self, cfg: SinkConfig, st: _SinkState) -> bool:
        try:
            return bool(cfg.is_ready_fn())  # type: ignore[arg-type]
        except Exception as e:
            st.last_err = f"is_ready: {e!r}"
            return False

    def _worker(self, name: str):
        cfg = self._cfgs[name]
        st  = self._states[name]
        q   = st.q

        # 主循环
        while not self._stop.is_set():
            try:
                table, data = q.get(timeout=0.1)
            except queue.Empty:
                continue
            if table is None and data is None:  # sentinel
                q.task_done()
                break

            # 迟连：没连上就按指数退避连接，直到连上或被停止
            if not self._ensure_connected(name, cfg, st):
                q.task_done()
                continue  # 正在停机，或外部打断

            # 发布 + 失败重试
            published = False
            attempts = cfg.retry_times + 1
            for i in range(attempts):
                try:
                    cfg.publish_fn(table, data)
                    st.sent += 1
                    published = True
                    st.last_err = None
                    break
                except cfg.recoverable as e:
                    st.errors += 1
                    st.last_err = f"recoverable: {e!r}"
                    # 标记断开，触发重连
                    st.connected = False
                    # 退避一点再重连
                    time.sleep(cfg.retry_backoff_s)
                    self._ensure_connected(name, cfg, st)
                    continue
                except Exception as e:
                    st.errors += 1
                    st.last_err = f"fatal: {e!r}"
                    logger.exception("sink %s fatal publish error: %r", name, e)
                    break

            # 失败后的回插策略
            if not published and cfg.requeue_on_failure:
                try:
                    q.put_nowait((table, data))
                except queue.Full:
                    st.dropped += 1

            q.task_done()