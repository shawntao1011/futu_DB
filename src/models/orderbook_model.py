from typing import Optional

from src.models.clean_model import CleanModel


class OrderBookModel(CleanModel):
    code : str
    name : str
    svr_recv_time_bid : str | None
    svr_recv_time_ask : str | None
    Bid: Optional[list[tuple[float, int, int, dict]]]
    Ask: Optional[list[tuple[float, int, int, dict]]]

    class Config:
        arbitrary_types_allowed = True
