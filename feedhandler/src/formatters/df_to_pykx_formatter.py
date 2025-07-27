from typing import Optional, Any

import pandas as pd
import pykx as kx


class DFToPykxFormatter:
    """
    1) 从扁平化 dict 构造 pandas.DataFrame
    2) 可选地把指定的 str 时间字段转成 pandas.Timestamp
    3) 根据field_map 重命名 并使用 field_map的顺序
    4) 调用 pykx.toq，传入业务侧的 ktype 映射，生成 kdb+ Table
    """
    def format(
            self,
            df: pd.DataFrame,
            ktype: Optional[dict[str, Any]] = None,
            time_fields: Optional[list[str]] = None,
            field_map: Optional[dict[str, str]] = None
    ) -> kx.Table:

        if time_fields:
            for col in time_fields:
                df[col] = pd.to_datetime(df[col])

        if field_map:
            df.rename(columns=field_map, inplace=True)
            df = df[field_map.keys()]

        if ktype:
            return kx.toq(df, ktype=ktype)
        else:
            return kx.toq(df)

