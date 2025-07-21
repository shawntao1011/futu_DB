from datetime import datetime
from typing import Optional, get_origin, get_args
from pydantic import BaseModel, root_validator


class CleanModel(BaseModel):
    class Config:
        extra = 'ignore'

    @root_validator(pre=True)
    def _clean_all(cls, values: dict) -> dict:
        cleaned = {}
        for name, raw in values.items():
            # 1) 空占位先变 None
            if raw in (None, '', 'N/A'):
                cleaned[name] = None
                continue

            field_info = cls.__fields__.get(name)
            if not field_info:
                cleaned[name] = raw
                continue

            expected = field_info.outer_type_
            # 如果 Optional[T]，取 T
            if get_origin(expected) is Optional:
                expected = get_args(expected)[0]

            # 3) 基础类型转换
            try:
                if expected is float:
                    cleaned[name] = float(raw)
                elif expected is int:
                    cleaned[name] = int(raw)
                elif expected is bool:
                    cleaned[name] = bool(raw)
                elif expected is datetime:
                    cleaned[name] = datetime.fromisoformat(raw)
                else:
                    cleaned[name] = raw
            except Exception:
                cleaned[name] = None

        return cleaned


class StockQuoteModel(CleanModel):
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
    turnover : float | None
    turnover_rate : float | None
    amplitude : int | None
    suspension : bool | None
    listing_date : str | None
    price_spread : float | None
    dark_status : str | None
    sec_status : str | None
    strike_price : float | None
    contract_size : float | None
    open_interest : int | None
    implied_volatility : float | None
    premium : float | None
    delta : float | None
    gamma : float | None
    vega : float | None
    theta : float | None
    rho : float | None
    index_option_type : str | None
    net_open_interest : int | None
    expiry_date_instance : int | None
    contract_nominal_value : float | None
    owner_lot_multiplier : float | None
    option_area_type : str | None
    contract_multiplier : float | None
    pre_price : float | None
    pre_high_price : float | None
    pre_low_price : float | None
    pre_volume : int | None
    pre_turnover : float | None
    pre_change_val : float | None
    pre_change_rate : float | None
    pre_amplitude : float | None
    after_price : float | None
    after_high_price : float | None
    after_low_price : float | None
    after_volume : int | None
    after_turnover : float | None
    after_change_val : float | None
    after_change_rate : float | None
    after_amplitude : float | None
    overnight_price : float | None
    overnight_high_price : float | None
    overnight_low_price : float | None
    overnight_volume : int | None
    overnight_turnover : float | None
    overnight_change_val : float | None
    overnight_change_rate : float | None
    overnight_amplitude : float | None
    last_settle_price : float | None
    position : float | None
    position_change : float | None

    class Config:
        arbitrary_types_allowed = True


class OrderBookModel(CleanModel):
    code : str
    name : str
    svr_recv_time_bid : str | None
    svr_recv_time_ask : str | None
    Bid : list | None
    Ask : list | None

    class Config:
        arbitrary_types_allowed = True

class CurKlineModel(CleanModel):
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
    k_type: str | None

    class Config:
        arbitrary_types_allowed = True

class RTDataModel(CleanModel):
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

    class Config:
        arbitrary_types_allowed = True

class TickerModel(CleanModel):
    code : str
    name : str
    sequence : int
    time : str
    price : float
    volume : int
    turnover : float
    ticker_direction : str | None
    type : str | None
    push_data_type : str | None

    class Config:
        arbitrary_types_allowed = True

class BrokerBidEntry(CleanModel):
    """买盘经纪队列一行"""
    code: str                   # 证券代码
    name: str                   # 证券名称
    bid_broker_id: int | None   # 买方经纪商 ID
    bid_broker_name: str | None # 买方经纪商名称
    bid_broker_pos: int | None  # 买方席位级别
    order_id: int | None        # 交易所订单号
    order_volume: int | None    # 订单未成交量

    class Config:
        arbitrary_types_allowed = True

class BrokerAskEntry(CleanModel):
    """卖盘经纪队列一行"""
    code: str
    name: str
    ask_broker_id: int | None
    ask_broker_name: str | None
    ask_broker_pos: int | None
    order_id: int | None
    order_volume: int | None

    class Config:
        arbitrary_types_allowed = True

class BrokerQueueModel(CleanModel):
    """一次完整的经纪队列推送"""
    stock_code: str                          # 订阅时的股票代码
    bid_frame: list[BrokerBidEntry] | None   # 所有买盘席位列表
    ask_frame: list[BrokerAskEntry] | None   # 所有卖盘席位列表

    class Config:
        arbitrary_types_allowed = True
