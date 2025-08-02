from src.models.clean_model import CleanModel

class TickerModel(CleanModel):
    code : str
    name : str
    sequence : int
    time : str
    price : float
    volume : float
    turnover : float
    ticker_direction : str | None
    type : str | None
    push_data_type : str | None

    class Config:
        arbitrary_types_allowed = True


FIELD_MAP = {
    "time"              :"time",
    "code"              :"sym",
    "name"              :"name",
    "price"             :"price",
    "volume"            :"volume",
    "turnover"          :"turnover",
    "ticker_direction"  :"tickDirection",
    "sequence"          :"sequence",
    "type"              :"tickType",
    "push_data_type"    :"srcType",
}