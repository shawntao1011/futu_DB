import logging

from futu import OrderBookHandlerBase, RET_ERROR, RET_OK
from pydantic import ValidationError

from src.formatters.df_to_pykx_formatter import DFToPykxFormatter
from src.models.orderbook_model import OrderBookModel
from src.models.orderbook_model import FIELD_MAP as ob_field_map
from src.publishers.tp_publisher import TPPublisher
from src.transformers.order_book_transformer import OrderBookTransformer

logger = logging.getLogger(__name__)

class OrderBookHandlerImpl(OrderBookHandlerBase):

    def __init__(
            self,
            transformer: OrderBookTransformer,
            formatter: DFToPykxFormatter,
            publisher: TPPublisher
    ):
        super().__init__()
        self.transformer = transformer
        self.formatter = formatter
        self.publisher = publisher

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

        # format to pykx table
        try:
            record = self.formatter.format(
                flat,
                None,
                time_fields=['time', 'svr_recv_time_bid', 'svr_recv_time_ask'],
                field_map=self.field_map,
            )
        except Exception as e:
            logger.error("format to pykx table failed: %s", e)
            return RET_ERROR, None

        try:
            self.publisher.publish("OrderBooks", record)
        except Exception as e:
            logger.error("publish record failed: %s", e)
            return RET_ERROR, None

        return RET_OK, data
