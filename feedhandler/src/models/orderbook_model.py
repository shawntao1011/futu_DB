from typing import Optional

from feedhandler.src.models.clean_model import CleanModel
from feedhandler.src.models.cur_kline_model import FIELD_MAP


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
    "code"              :"sym",
    "time"              :"time",
    "svr_recv_time_bid" :"bidTime",
    "svr_recv_time_ask" :"askTime",
    "bid1_price"        :"bid1Price",
    "bid2_price"        :"bid2Price",
    "bid3_price"        :"bid3Price",
    "bid4_price"        :"bid4Price",
    "bid5_price"        :"bid5Price",
    "bid6_price"        :"bid6Price",
    "bid7_price"        :"bid7Price",
    "bid8_price"        :"bid8Price",
    "bid9_price"        :"bid9Price",
    "bid10_price"       :"bid10Price",
    "bid1_volume"       :"bid1Volume",
    "bid2_volume"       :"bid2Volume",
    "bid3_volume"       :"bid3Volume",
    "bid4_volume"       :"bid4Volume",
    "bid5_volume"       :"bid5Volume",
    "bid6_volume"       :"bid6Volume",
    "bid7_volume"       :"bid7Volume",
    "bid8_volume"       :"bid8Volume",
    "bid9_volume"       :"bid9Volume",
    "bid10_volume"      :"bid10Volume",
    "bid1_qty"          :"bid1Qty",
    "bid2_qty"          :"bid2Qty",
    "bid3_qty"          :"bid3Qty",
    "bid4_qty"          :"bid4Qty",
    "bid5_qty"          :"bid5Qty",
    "bid6_qty"          :"bid6Qty",
    "bid7_qty"          :"bid7Qty",
    "bid8_qty"          :"bid8Qty",
    "bid9_qty"          :"bid9Qty",
    "bid10_qty"         :"bid10Qty",
    "ask1_price"        :"ask1Price",
    "ask2_price"        :"ask2Price",
    "ask3_price"        :"ask3Price",
    "ask4_price"        :"ask4Price",
    "ask5_price"        :"ask5Price",
    "ask6_price"        :"ask6Price",
    "ask7_price"        :"ask7Price",
    "ask8_price"        :"ask8Price",
    "ask9_price"        :"ask9Price",
    "ask10_price"       :"ask10Price",
    "ask1_volume"       :"ask1Volume",
    "ask2_volume"       :"ask2Volume",
    "ask3_volume"       :"ask3Volume",
    "ask4_volume"       :"ask4Volume",
    "ask5_volume"       :"ask5Volume",
    "ask6_volume"       :"ask6Volume",
    "ask7_volume"       :"ask7Volume",
    "ask8_volume"       :"ask8Volume",
    "ask9_volume"       :"ask9Volume",
    "ask10_volume"      :"ask10Volume",
    "ask1_qty"          :"ask1Qty",
    "ask2_qty"          :"ask2Qty",
    "ask3_qty"          :"ask3Qty",
    "ask4_qty"          :"ask4Qty",
    "ask5_qty"          :"ask5Qty",
    "ask6_qty"          :"ask6Qty",
    "ask7_qty"          :"ask7Qty",
    "ask8_qty"          :"ask8Qty",
    "ask9_qty"          :"ask9Qty",
    "ask10_qty"         :"ask10Qty",
}