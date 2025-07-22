from typing import Optional, Any

import pandas as pd
import pykx as kx


class DictToPykxFormatter:
    """
    1) 从扁平化 dict 构造 pandas.DataFrame
    2) 可选地把指定的 str 时间字段转成 pandas.Timestamp
    3) 调用 pykx.toq，传入业务侧的 ktype 映射，生成 kdb+ Table
    """
    def format(
            self,
            data: dict[str, Any],
            ktype: Optional[dict[str, Any]] = None,
            time_fields: Optional[list[str]] = None,
            parse_times: Optional[bool] = None
    ) -> kx.Table:

        if parse_times:
            for col in time_fields:
                val = data.get(col)
                if isinstance(val, str):
                    data[col] = pd.to_datetime(val)

        df = pd.DataFrame([data])
        tbl = kx.toq(df, ktype=ktype)
        return tbl
