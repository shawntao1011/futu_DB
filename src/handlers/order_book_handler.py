import logging

from futu import OrderBookHandlerBase, RET_ERROR, RET_OK
from jsonschema import ValidationError

from src.formatters.dict_to_pykx_formatter import DictToPykxFormatter
from src.models.orderbook_model import OrderBookModel
from src.publishers.tp_publisher import TPPublisher
from src.transformers.order_book_transformer import OrderBookTransformer

import pykx as kx

logger = logging.getLogger(__name__)

class OrderBookHandlerImpl(OrderBookHandlerBase):

    def __init__(
            self,
            transformer: OrderBookTransformer,
            formatter: DictToPykxFormatter,
            publisher: TPPublisher
    ):
        super().__init__()
        self.transformer = transformer
        self.formatter = formatter
        self.publisher = publisher


    def on_recv_rsp(self, rsp_pb):
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
            flat = self.transformer.pivot(raw)
        except Exception as e:
            logger.error("transform to pivot dict failed: %s", e)
            return RET_ERROR, None

        # format to pykx table
        try:
            tbl = self.formatter.format(
                flat,
                ktype={
                    'code': kx.SymbolAtom,
                    'name': kx.CharVector,
                    'svr_recv_time_bid': kx.TimestampAtom,
                    'svr_recv_time_ask': kx.TimestampAtom,
                },
                time_fields=['svr_recv_time_bid', 'svr_recv_time_ask'],
                parse_times=True
            )
        except Exception as e:
            logger.error("format to pykx table failed: %s", e)
            return RET_ERROR, None

        try:
            self.publisher.publish(tbl)
        except Exception as e:
            logger.error("publish table failed: %s", e)
            return RET_ERROR, None

        return RET_OK, data
