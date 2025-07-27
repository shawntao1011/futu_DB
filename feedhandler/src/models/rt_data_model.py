from src.models.clean_model import CleanModel


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
