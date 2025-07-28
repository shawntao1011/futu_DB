from typing import Optional, Any

import pandas as pd
import pykx as kx


class DictToPykxFormatter:
    """
    1) 可选地把指定的 str 时间字段转成 pandas.Timestamp
    2) 从扁平化 dict 构造 pd.DataFrame
    3) 根据field_map 重命名 并使用 field_map的顺序
    4) 将 pd.DataFrame 转换成 pykx.Table 并做相应的ktype转化
    """
    def format(
            self,
            data: dict[str, Any],
            ktype: Optional[dict[str, Any]] = None,
            time_fields: Optional[list[str]] = None,
            field_map: Optional[dict[str, str]] = None
    ) -> kx.Table:

        if time_fields:
            for col in time_fields:
                val = data.get(col)
                if isinstance(val, str):
                    data[col] = pd.to_datetime(val)

        df = pd.DataFrame([data])

        if field_map:
            df.rename(columns=field_map, inplace=True)
            df = df[field_map.values()]

        if ktype:
            return kx.toq(df, ktype=ktype)
        else:
            return kx.toq(df)

