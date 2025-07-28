from typing import Optional

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

    def pivot(self, raw: dict[str, any]):

        for key in ("code", "name", "svr_recv_time_bid", "svr_recv_time_ask", "Bid", "Ask"):
            if key not in raw:
                raise ValueError(f"Missing required field: {key}")

        bid_time_str = raw.get("svr_recv_time_bid")
        ask_time_str = raw.get("svr_recv_time_ask")

        flat: dict[str, any] = {
            "code": raw["code"],
            "time": self.pick_time_str(bid_time_str, ask_time_str),
            "name": raw["name"],
            "svr_recv_time_bid": bid_time_str,
            "svr_recv_time_ask": ask_time_str,
            "Bid": raw.get("Bid"),
            "Ask": raw.get("Ask")
        }

        for side in ("Bid", "Ask"):
            entries = raw.get(side) or []
            for i in range(1, self.depth + 1):
                try:
                    price, volume, qty, _ = entries[i-1]
                except IndexError:
                    price, volume, qty, _ = None, None, None, None

                flat[f"{side.lower()}{i}_price"] = price
                flat[f"{side.lower()}{i}_volume"] = volume
                flat[f"{side.lower()}{i}_qty"] = qty

        flat.pop("Bid")
        flat.pop("Ask")

        return flat