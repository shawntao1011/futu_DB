

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

    def pivot(self, raw: dict[str, any]):

        for key in ("code", "name", "svr_recv_time_bid", "svr_recv_time_ask", "Bid", "Ask"):
            if key not in raw:
                raise ValueError(f"Missing required field: {key}")

        flat: dict[str, any] = {
            "code": raw["code"],
            "name": raw["name"],
            "svr_recv_time_bid": raw["svr_recv_time_bid"],
            "svr_recv_time_ask": raw["svr_recv_time_ask"],
            "Bid": raw.get("Bid"),
            "Ask": raw.get("Ask")
        }

        for side in ("Bid", "Ask"):
            entries = raw.get(side) or []
            for i in range(1, self.depth + 1):
                try:
                    price, volume, qty = entries[i-1]
                except IndexError:
                    price, volume, qty = None, None, None

                flat[f"{side.lower()}{i}_price"] = price
                flat[f"{side.lower()}{i}_volume"] = volume
                flat[f"{side.lower()}{i}_qty"] = qty

        flat.pop("Bid")
        flat.pop("Ask")

        return flat