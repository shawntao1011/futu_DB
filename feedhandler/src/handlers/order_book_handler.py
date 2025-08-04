import logging

from futu import OrderBookHandlerBase, RET_ERROR, RET_OK
from pydantic import ValidationError

import pykx as kx

from src.cleaners.dataframe_cleaner import DataFrameCleaner
from src.formatters.df_to_updx_formatter import DFToUpdXFormatter
from src.models.orderbook_model import OrderBookModel
from src.models.orderbook_model import FIELD_MAP as ob_field_map
from src.publishers.tp_publisher import TPPublisher
from src.transformers.order_book_transformer import OrderBookTransformer

logger = logging.getLogger(__name__)

class OrderBookHandlerImpl(OrderBookHandlerBase):

    def __init__(
            self,
            transformer: OrderBookTransformer,
            cleaner: DataFrameCleaner,
            formatter: DFToUpdXFormatter,
            publisher: TPPublisher
    ):
        super().__init__()
        self.transformer = transformer
        self.formatter = formatter
        self.publisher = publisher
        self.cleaner = cleaner

        self.field_map = ob_field_map

    # https://openapi.futunn.com/futu-api-doc/en/quote/update-order-book.html
    def on_recv_rsp(self, rsp_pb):
        # return type: dict
        ret_code, data = super(OrderBookHandlerImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        try:
            obm = OrderBookModel(**data)
        except ValidationError as err:
            logger.warning("invalid order book record: %s", data)
            return RET_ERROR, None

        raw = obm.dict()

        # transform to flat table
        try:
            # dict flat to dataframe
            flat = self.transformer.flat(raw)
        except Exception as e:
            logger.error("transform to pivot dict failed: %s", e)
            return RET_ERROR, None

        cleaned_df = self.cleaner.clean(
            flat,
            {
                'time': 'datetime64[ns]',
                'code': 'string',
                'name': 'string',
                'level': 'Int32',
                'svr_recv_time_bid': 'datetime64[ns]',
                'bid_price': 'float',
                'bid_volume': 'float',
                'bid_qty': 'float',
                'svr_recv_time_ask': 'datetime64[ns]',
                'ask_price': 'float',
                'ask_volume': 'float',
                'ask_qty': 'float'
            })

        # format to pykx table
        try:
            tbl = self.formatter.format(
                cleaned_df,
                ktype={
                    'level': kx.IntVector,
                },
                field_map=self.field_map,
            )
        except Exception as e:
            logger.error("format to pykx table failed: %s", e)
            return RET_ERROR, None

        try:
            self.publisher.publish("OrderBooks", tbl)
        except Exception as e:
            logger.error("publish record failed: %s", e)
            return RET_ERROR, None

        return RET_OK, data
