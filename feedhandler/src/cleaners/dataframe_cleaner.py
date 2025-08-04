from typing import Any

import pandas as pd

def _ensure_list(x):
    if x is None:
        return []
    if isinstance(x, str):
        return [x]
    try:
        return list(x)
    except:
        return [x]

class DataFrameCleaner:
    class DataFrameCleaner:
        """
        Cleans a pandas DataFrame by replacing None with pandas <NA>,
        and converting specified columns to user-defined pandas/numpy dtypes.

        :param dtype_map: Mapping of column names to target dtypes.
                          Supported dtypes: numpy dtypes (e.g. 'int64', 'float32'),
                          pandas nullable dtypes (e.g. 'Int64', 'string'),
                          datetime dtypes (e.g. 'datetime64[ns]').
        """

    def clean(
            self,
            df: pd.DataFrame,
            dtype_map: dict[str, Any]
    ) -> pd.DataFrame:

        df2 = df.copy()
        # 1) Replace Python None and NaN with pandas <NA>
        df2 = df2.where(df2.notna(), pd.NA)

        # 2) Convert specified columns
        for col, target_dtype in dtype_map.items():
            if col not in df2.columns:
                continue
            # Interpret target_dtype via pandas api
            try:
                pd_dtype = pd.api.types.pandas_dtype(target_dtype)
            except TypeError:
                # invalid dtype specification, skip
                continue

            # Apply conversion based on dtype kind
            if pd.api.types.is_datetime64_any_dtype(pd_dtype):
                # datetime
                df2[col] = pd.to_datetime(df2[col], errors='coerce')
            elif pd.api.types.is_integer_dtype(pd_dtype):
                # nullable integer (Int64) or numpy int
                # coerce to numeric then astype
                series = pd.to_numeric(df2[col], errors='coerce')
                df2[col] = series.astype(pd_dtype)
            elif pd.api.types.is_float_dtype(pd_dtype):
                # float
                series = pd.to_numeric(df2[col], errors='coerce')
                df2[col] = series.astype(pd_dtype)
            else:
                # treat as string or other category
                try:
                    df2[col] = df2[col].astype(pd_dtype)
                except Exception:
                    # fallback: cast to pandas StringDtype
                    df2[col] = df2[col].astype('string')

        return df2
