import logging
import pykx as kx

from futu import CurKlineHandlerBase, RET_OK, RET_ERROR
from pydantic import parse_obj_as, ValidationError

from src.formatters.df_to_pykx_formatter import DFToPykxFormatter
from src.models.cur_kline_model import CurKlineModel
from src.models.cur_kline_model import FIELD_MAP as ckline_field_map
from src.publishers.tp_publisher import TPPublisher

logger = logging.getLogger(__name__)

class CurKlineHandlerImpl(CurKlineHandlerBase):

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

        self.field_map = ckline_field_map

    # https://openapi.futunn.com/futu-api-doc/en/quote/update-kl.html
    def on_recv_rsp(self, rsp_pb):
        # return data : DataFrame
        ret_code, data = super(CurKlineHandlerImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        try:
            parse_obj_as(list[CurKlineModel], data.to_dict('records'))
        except ValidationError as err:
            logger.warning("invalid curkline record: %s", data)
            return RET_ERROR, None

        # no need to transform

        # format to pykx table
        try:
            tbl = self.formatter.format(
                data,
                ktype={
                    'time': kx.TimestampAtom,
                },
                time_fields=['time_key'],
                field_map=self.field_map
            )
        except Exception as e:
            logger.error("format to pykx table failed: %s", e)
            return RET_ERROR, None

        try:
            self.publisher.publish("Minutes", tbl)
        except Exception as e:
            logger.error("publish table failed: %s", e)

        return RET_OK, data


