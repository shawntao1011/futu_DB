from feedhandler.src.models.clean_model import CleanModel


class CurKlineModel(CleanModel):
    code : str
    name : str
    time_key : str
    open : float
    close : float
    high : float
    low : float
    volume : float
    turnover : float
    pe_ratio : float
    turnover_rate : float
    last_close : float
    k_type: str | None

    class Config:
        arbitrary_types_allowed = True

# kdb q field map
FIELD_MAP = {
    "code":         "sym",
    "time_key":     "time",
    "name":         "name",
    "open":         "open",
    "close":        "close",
    "high":         "high",
    "low":          "low",
    "volume":       "volume",
    "turnover":     "turnover",
    "k_type":       "kType",
    "pe_ratio":     "peRatio",
    "turnover_rate":"turnoverRate",
    "last_close":   "lastClose",
}