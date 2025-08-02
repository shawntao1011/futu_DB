from typing import Optional, Any

import pandas as pd
import pykx as kx


class DFToPykxFormatter:
    """
    1) 可选地把指定的 str 时间字段转成 pandas.Timestamp
    2) 根据field_map 重命名 并使用 field_map的顺序
    3) 调用 pykx.toq，传入业务侧的 ktype 映射，生成 kdb+ Table
    4) 为了迎合 .u.upd 的 convention， 转化成 list of columns
    """
    def format(
            self,
            df: pd.DataFrame,
            ktype: Optional[dict[str, Any]] = None,
            time_fields: Optional[list[str]] = None,
            field_map: Optional[dict[str, str]] = None
    ) -> kx.List:

        if time_fields:
            for col in time_fields:
                df[col] = pd.to_datetime(df[col])

        if field_map:
            df.rename(columns=field_map, inplace=True)
            df = df[field_map.values()]

        list_of_columns = kx.toq(df.values.T)

        field_map_ids = {k: i for i, k in enumerate(field_map.keys())}

        if ktype:
            common_keys = field_map.keys() & ktype.keys()

            applied_ktype = { field_map_ids[k]: ktype[k] for k in common_keys }
            if applied_ktype:
                for k, v in applied_ktype.items():
                    if not isinstance(list_of_columns[k], v):
                        list_of_columns[k] = kx.toq(list_of_columns[k], ktype=v)

        return list_of_columns






