from typing import Optional, Any

import pandas as pd
import pykx as kx


class DFToUpdXFormatter:
    """
    1) 可选地把指定的 str 时间字段转成 pandas.Timestamp
    2) 根据field_map 重命名 并使用 field_map的顺序
    3) 调用 pykx.toq，传入业务侧的 ktype 映射，生成 kdb+ Table
    4) 为了迎合 .u.upd 的 convention， 转化成 list of columns
    """
    def format(
            self,
            df: pd.DataFrame,
            ktype: dict[str, Any] | None,
            field_map: dict[str, str] | None
    ) -> kx.List:

        df2 = df.copy()

        if field_map:
            df2 = df2.rename(columns=field_map)
            df2 = df2[[new_name for new_name in field_map.values()]]

        if ktype:
            tbl = kx.toq(df2, ktype=ktype)
        else:
            tbl = kx.toq(df2)

        cols = df2.columns

        return kx.q.flip(tbl)[cols]


