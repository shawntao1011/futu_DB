import logging

import pandas as pd
import pykx as kx

from futu import TickerHandlerBase, RET_OK, RET_ERROR
from pydantic import parse_obj_as, ValidationError

from src.cleaners.dataframe_cleaner import DataFrameCleaner
from src.formatters.df_to_updx_formatter import DFToUpdXFormatter
from src.models.ticker_model import TickerModel
from src.models.ticker_model import FIELD_MAP as tick_field_map
from src.publishers.tp_publisher import TPPublisher

logger = logging.getLogger(__name__)

class TickerHandlerImpl(TickerHandlerBase):

    def __init__(
            self,
            transformer: None,
            cleaner: DataFrameCleaner,
            formatter: DFToUpdXFormatter,
            publisher: TPPublisher
    ):
        super().__init__()
        self.transformer = transformer
        self.formatter = formatter
        self.publisher = publisher
        self.cleaner = cleaner

        self.field_map = tick_field_map

    # https://openapi.futunn.com/futu-api-doc/en/quote/update-ticker.html
    def on_recv_rsp(self, rsp_pb):
        # return data : pd.DataFrame
        ret_code, data = super(TickerHandlerImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        try:
            models: list[TickerModel] = parse_obj_as(list[TickerModel], data.to_dict('records'))
        except ValidationError as err:
            logger.warning("invalid tick record: %s", data)
            return RET_ERROR, None

        df = pd.DataFrame.from_records([m.dict() for m in models])
        # no need to transform

        # clean data
        cleaned_df = self.cleaner.clean(
            df,
            {
                'time': 'datetime64[ns]',
                'code': 'string',
                'name': 'string',
                'price': 'float',
                'volume': 'float',
                'turnover': 'float',
                'ticker_direction': 'string',
                'sequence': 'Int64',
                'type': 'string',
                'push_data_type': 'string'
            }
        )

        # format to pykx table
        try:
            tbl = self.formatter.format(
                cleaned_df,
                ktype={
                    'time': kx.TimestampVector,
                },
                field_map=self.field_map
            )
        except Exception as e:
            logger.error("format to pykx table failed: %s", e)
            return RET_ERROR, None

        try:
            self.publisher.publish("Ticks", tbl)
        except Exception as e:
            logger.error("publish table failed: %s", e)
            return RET_ERROR, None

        return RET_OK, data