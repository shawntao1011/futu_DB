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

# kdb column map to OrderBooks
FIELD_MAP = {
    "time"              :"time",
    "code"              :"sym",
    "svr_recv_time_bid" :"bidTime",
    "svr_recv_time_ask" :"askTime",
    "level"             :"level",
    "bid_price"         :"bidPrice",
    "bid_volume"        :"bidVolume",
    "bid_qty"           :"bidQty",
    "ask_price"         :"askPrice",
    "ask_volume"        :"askVolume",
    "ask_qty"           :"askQty"
}