import logging
import pykx as kx

from futu import TickerHandlerBase, RET_OK, RET_ERROR
from jsonschema import ValidationError
from pydantic import parse_obj_as

from src.formatters.df_to_pykx_formatter import DFToPykxFormatter
from src.models.ticker_model import TickerModel
from src.publishers.tp_publisher import TPPublisher

logger = logging.getLogger(__name__)

class TickerHandlerImpl(TickerHandlerBase):

    def __init__(
            self,
            transformer: None,
            formatter: DFToPykxFormatter,
            publisher: TPPublisher
    ):
        super().__init__()
        self.transformer = transformer
        self.formatter = formatter
        self.publisher = publisher

    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(TickerHandlerImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        try:
            parse_obj_as(list[TickerModel], data.to_dict('records'))
        except ValidationError as err:
            logger.warning("invalid tick record: %s", data)
            return RET_ERROR, None

        # no need to transform

        # format to pykx table
        try:
            tbl = self.formatter.format(
                data,
                ktype={
                    'code': kx.SymbolAtom,
                    'name': kx.CharVector,
                    'time': kx.TimestampAtom,
                },
                time_fields=['time'],
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