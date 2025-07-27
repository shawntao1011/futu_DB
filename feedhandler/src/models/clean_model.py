from datetime import datetime
from typing import Optional, get_origin, get_args

from pydantic import BaseModel, root_validator


class CleanModel(BaseModel):
    class Config:
        extra = 'ignore'

    @root_validator(pre=True)
    def _clean_all(cls, values: dict) -> dict:
        cleaned = {}
        for name, raw in values.items():
            # 1) 空占位先变 None
            if raw in (None, '', 'N/A'):
                cleaned[name] = None
                continue

            field_info = cls.__fields__.get(name)
            if not field_info:
                cleaned[name] = raw
                continue

            expected = field_info.outer_type_
            # 如果 Optional[T]，取 T
            if get_origin(expected) is Optional:
                expected = get_args(expected)[0]

            # 3) 基础类型转换
            try:
                if expected is float:
                    cleaned[name] = float(raw)
                elif expected is int:
                    cleaned[name] = int(raw)
                elif expected is bool:
                    cleaned[name] = bool(raw)
                elif expected is datetime:
                    cleaned[name] = datetime.fromisoformat(raw)
                else:
                    cleaned[name] = raw
            except Exception:
                cleaned[name] = None

        return cleaned