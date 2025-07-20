from fastapi.params import Security
from futu import DarkStatus, SecurityStatus, IndexOptionType, OptionAreaType, KLType, TickerDirect, TickerType, \
    PushDataType
from pydantic import BaseModel


class StockQuoteModel(BaseModel):
    code : str
    name : str
    data_date : str
    data_time : str
    last_price : float
    open_price : float
    high_price : float
    low_price : float
    prev_close_price : float
    volume : int
    turnover : float
    turnover_rate : float
    amplitude : int
    suspension : bool
    listing_date : str
    price_spread : float
    dark_status : DarkStatus
    sec_status : SecurityStatus
    strike_price : float
    contract_size : float
    open_interest : int
    implied_volatility : float
    premium : float
    delta : float
    gamma : float
    vega : float
    theta : float
    rho : float
    index_option_type : IndexOptionType
    net_open_interest : int
    expiry_date_instance : int
    contract_nominal_value : float
    owner_lot_multiplier : float
    option_area_type : OptionAreaType
    contract_multiplier : float
    pre_price : float
    pre_high_price : float
    pre_low_price : float
    pre_volume : int
    pre_turnover : float
    pre_change_val : float
    pre_change_rate : float
    pre_amplitude : float
    after_price : float
    after_high_price : float
    after_low_price : float
    after_volume : int
    after_turnover : float
    after_change_val : float
    after_change_rate : float
    after_amplitude : float
    overnight_price : float
    overnight_high_price : float
    overnight_low_price : float
    overnight_volume : int
    overnight_turnover : float
    overnight_change_val : float
    overnight_change_rate : float
    overnight_amplitude : float
    last_settle_price : float
    position : float
    position_change : float


class OrderBookModel(BaseModel):
    code : str
    name : str
    svr_recv_time_bid : str
    svr_receive_time_ask : str
    Bid : list
    Ask : list

class CurKlineModel(BaseModel):
    code : str
    name : str
    time_key : str
    open : float
    close : float
    high : float
    low : float
    volume : int
    turnover : float
    pe_ratio : float
    turnover_rate : float
    last_close : float
    k_type: KLType

class RTDataModel(BaseModel):
    code : str
    name : str
    time : str
    is_blank : bool
    opened_mins : int
    cur_price : float
    last_close : float
    avg_price : float
    volume : float
    turnover : float

class TickerModel(BaseModel):
    code : str
    name : str
    sequence : int
    time : str
    price : float
    volume : int
    turnover : float
    ticker_direction : TickerDirect
    type : TickerType
    push_data_type : PushDataType

class BrokerBidEntry(BaseModel):
    """买盘经纪队列一行"""
    code: str               # 证券代码
    name: str               # 证券名称
    bid_broker_id: int      # 买方经纪商 ID
    bid_broker_name: str    # 买方经纪商名称
    bid_broker_pos: int     # 买方席位级别
    order_id: int           # 交易所订单号
    order_volume: int       # 订单未成交量

class BrokerAskEntry(BaseModel):
    """卖盘经纪队列一行"""
    code: str
    name: str
    ask_broker_id: int
    ask_broker_name: str
    ask_broker_pos: int
    order_id: int
    order_volume: int

class BrokerQueueModel(BaseModel):
    """一次完整的经纪队列推送"""
    stock_code: str                   # 订阅时的股票代码
    bid_frame: list[BrokerBidEntry]   # 所有买盘席位列表
    ask_frame: list[BrokerAskEntry]   # 所有卖盘席位列表