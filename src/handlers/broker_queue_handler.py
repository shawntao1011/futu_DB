import logging
import pykx as kx

from futu import BrokerHandlerBase, RET_OK, RET_ERROR
from jsonschema import ValidationError
from pydantic import parse_obj_as

from src.formatters.df_to_pykx_formatter import DFToPykxFormatter
from src.models.broker_queue_model import BrokerBidEntry, BrokerAskEntry
from src.publishers.tp_publisher import TPPublisher
from src.transformers.broker_queue_transformer import BrokerQueueTransformer

logger = logging.getLogger(__name__)

class BrokerQueueHandlerImpl(BrokerHandlerBase):

    def __init__(
            self,
            transformer: BrokerQueueTransformer,
            formatter: DFToPykxFormatter,
            publisher: TPPublisher
    ):
        super().__init__()
        self.transformer = transformer
        self.formatter = formatter
        self.publisher = publisher

    def on_recv_rsp(self, rsp_pb):
        ret_code, err_or_code, data = super(BrokerQueueHandlerImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        try:
            parse_obj_as(list[BrokerBidEntry], data[1].to_dict('records'))
            parse_obj_as(list[BrokerAskEntry], data[2].to_dict('records'))
        except ValidationError as err:
            logger.warning("invalid order queue record: %s", data)
            return RET_ERROR, None

        try:
            df = self.transformer.flattern(data)
        except Exception as e:
            logger.error("transform to flat table failed: %s", e)
            return RET_ERROR, None

        try:
            tbl = self.formatter.format(
                df,
                ktype={
                    'code': kx.SymbolAtom,
                    'name': kx.CharVector,
                    'time': kx.TimestampAtom,
                    'broker_name': kx.SymbolAtom,
                    'side': kx.SymbolAtom
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






