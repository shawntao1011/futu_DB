import logging
import os
import pykx as kx
from pykx import SyncQConnection

class TPPublisher:
    """
    Publisher for sending PyKX Table data to kdb+ tickerplant via IPC using SyncQConnection
    with automatic reconnect support. On failure, archives to CSV fallback_dir.

    Usage:
        pub = TPPublisher(
            host="localhost", port=5010,
            username="", password="",
            wait=True,
            reconnection_attempts=-1, reconnection_delay=0.5,
            fallback_dir="failed"
        )
        pub.publish("orderbook", pykx_table)
    """
    def __init__(
        self,
        host: str = "localhost",
        port: int = None,
        username: str = "",
        password: str = "",
        timeout: float = 0.0,
        large_messages: bool = True,
        tls: bool = False,
        unix: bool = False,
        wait: bool = True,
        no_ctx: bool = False,
        reconnection_attempts: int = -1,
        reconnection_delay: float = 0.5,
        reconnection_function = None,
        fallback_dir: str | None = None
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.info("Connecting to tickerplant %s:%s", host, port)
        try:
            self.conn = SyncQConnection(
                host=host,
                port=port,
                username=username,
                password=password,
                timeout=timeout,
                large_messages=large_messages,
                tls=tls,
                unix=unix,
                wait=wait,
                no_ctx=no_ctx,
                reconnection_attempts=reconnection_attempts,
                reconnection_delay=reconnection_delay,
                reconnection_function=reconnection_function
            )
        except Exception as e:
            self.logger.error(f'Failed to connect to tickerplant {host}:{port}: {e}')
        self.logger.info("TPPublisher connected to %s:%s", host, port)

        self.fallback_dir = fallback_dir
        if fallback_dir:
            os.makedirs(fallback_dir, exist_ok=True)

    def publish(
        self,
        table: str,
        tbl: kx.Table,
        wait: bool | None = False,
    ) -> None:
        """
        Publish a PyKX Table to tickerplant via .u.upd.

        :param table: target kdb+ table name
        :param tbl:   pykx.Table instance
        :param wait:  override wait flag for this call
        """
        rows = len(tbl)
        self.logger.info("Publishing %d rows to '%s'", rows, table)
        try:
            self.conn('.u.upd', kx.toq(table), tbl, wait=wait)
            self.logger.debug("Published %d rows to '%s'", rows, table)
        except Exception as e:
            self.logger.error(f"Failed to publish to '{table}': {e!r}", exc_info=True)
            if self.fallback_dir:
                try:
                    df = tbl.pd()
                    path = os.path.join(self.fallback_dir, f"{table}.csv")
                    write_header = not os.path.exists(path)
                    df.to_csv(
                        path,
                        mode='a',
                        index=False,
                        header=write_header,
                        encoding='utf-8-sig'
                    )
                    self.logger.info(f"Archived {len(df)} rows to {path}")
                except Exception as arch_exc:
                    self.logger.error(f"Failed to archive to {path}: {arch_exc!r}")
            else:
                self.logger.warning("No fallback_dir set; failed batch dropped")