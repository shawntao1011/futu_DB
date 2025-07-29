from typing import Optional, Any

import pandas as pd


class OrderBookTransformer:
    """
    将标准化的 OrderBookModel.dict() 输出扁平化字典:
      ask1_price, ask1_volume, ask1_qty,
      ...
      ask10_price, ask10_volume, ask10_qty,
      bid1_price, bid1_volume, bid1_qty,
      ...
      bid10_price, bid10_volume, bid10_qty
    """
    def __init__(self, depth: int = 10):
        self.depth = depth

    def pick_time_str(
            self,
            bid: Optional[str],
            ask: Optional[str]
    ) -> Optional[str]:
        """
        从两个 ISO 时间字符串中取最早的那个，若只有一个非 None 则返回它，
        若都为 None 则返回 None。
        """
        if bid is None:
            return ask
        if ask is None:
            return bid
        # ISO 字符串可以直接字典序比较
        return bid if bid <= ask else ask

    def flat(self, raw: dict[str, any]):

        for key in ("code", "name", "svr_recv_time_bid", "svr_recv_time_ask", "Bid", "Ask"):
            if key not in raw:
                raise ValueError(f"Missing required field: {key}")

        bid_time_str = raw.get("svr_recv_time_bid")
        ask_time_str = raw.get("svr_recv_time_ask")

        time = self.pick_time_str(bid_time_str, ask_time_str)
        code = raw["code"]
        name = raw["name"]

        records: list[dict[str, Any]] = []
        bids = raw.get("Bid") or []
        asks = raw.get("Ask") or []
        for lvl in range(1, self.depth + 1):
            # 取第 lvl 档，IndexError 则补 None
            try:
                bp, bv, bq, _ = bids[lvl - 1]
            except (IndexError, ValueError):
                bp = bv = bq = None
            try:
                ap, av, aq, _ = asks[lvl - 1]
            except (IndexError, ValueError):
                ap = av = aq = None

            records.append({
                "code": code,
                "name": name,
                "time": time,
                "svr_recv_time_bid": bid_time_str,
                "svr_recv_time_ask": ask_time_str,
                "level": lvl,
                "bid_price": bp,
                "bid_volume": bv,
                "bid_qty": bq,
                "ask_price": ap,
                "ask_volume": av,
                "ask_qty": aq,
            })

        return pd.DataFrame(records)