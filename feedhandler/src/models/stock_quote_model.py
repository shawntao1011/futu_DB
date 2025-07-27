from feedhandler.src.models.clean_model import CleanModel


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