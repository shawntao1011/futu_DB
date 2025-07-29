from src.models.clean_model import CleanModel

class BrokerBidEntry(CleanModel):
    """买盘经纪队列一行"""
    code: str                   # 证券代码
    name: str                   # 证券名称
    bid_broker_id: int | None   # 买方经纪商 ID
    bid_broker_name: str | None # 买方经纪商名称
    bid_broker_pos: float | None  # 买方席位级别
    order_id: int | None        # 交易所订单号
    order_volume: float | None    # 订单未成交量

    class Config:
        arbitrary_types_allowed = True

class BrokerAskEntry(CleanModel):
    """卖盘经纪队列一行"""
    code: str
    name: str
    ask_broker_id: int | None
    ask_broker_name: str | None
    ask_broker_pos: float | None
    order_id: int | None
    order_volume: float | None

    class Config:
        arbitrary_types_allowed = True

class BrokerQueueModel(CleanModel):
    """一次完整的经纪队列推送"""
    stock_code: str                          # 订阅时的股票代码
    bid_frame: list[BrokerBidEntry] | None   # 所有买盘席位列表
    ask_frame: list[BrokerAskEntry] | None   # 所有卖盘席位列表

    class Config:
        arbitrary_types_allowed = True

# kdb q field map
FIELD_MAP = {
    "time":         "time",
    "code":         "sym",
    "name":         "name",
    "broker_id":    "brokerId",
    "broker_name":  "brokerName",
    "broker_pos":   "brokerPos",
    "order_id":     "orderId",
    "order_volume": "orderVolume",
    "side":         "side",
}