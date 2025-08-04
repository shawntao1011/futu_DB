from collections import OrderedDict
from typing import Optional, Any

import pandas as pd
import pykx as kx

class DictToUpdXFormatter:
    """
    1) 可选地把指定的 str 时间字段转成 pandas.Timestamp
    2) 根据field_map 重命名 并使用 field_map的顺序
    3) 将 pd.DataFrame 转换成 pykx.Table 并做相应的ktype转化
    """
    def format(
            self,
            data: dict[str, Any],
            ktype: Optional[dict[str, Any]] = None,
            time_fields: Optional[list[str]] = None,
            field_map: Optional[dict[str, str]] = None
    ) -> kx.List:

        if time_fields:
            for col in time_fields:
                val = data.get(col)
                if isinstance(val, str):
                    data[col] = pd.to_datetime(val)

        if field_map:
            reordered = {field_map[key]: data[key] for key in field_map.keys()}
            data = reordered

        kx_dict = kx.toq(data)

        common_keys = field_map.keys() & ktype.keys()
        applied_ktype= {k: ktype[k] for k in common_keys}
        if applied_ktype:
            for k, v in applied_ktype.items():
                if not isinstance(kx_dict.get(k), v):
                    kx_dict[k] = kx.toq(kx_dict.get(k), ktype=v)

        return kx_dict




