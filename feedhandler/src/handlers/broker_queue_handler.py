import logging

import pandas as pd
import pykx as kx

from futu import BrokerHandlerBase, RET_OK, RET_ERROR
from pydantic import parse_obj_as, ValidationError

from src.formatters.df_to_pykx_formatter import DFToPykxFormatter
from src.models.broker_queue_model import BrokerBidEntry, BrokerAskEntry
from src.models.broker_queue_model import FIELD_MAP as bq_field_map
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

        self.field_map = bq_field_map

    # https://openapi.futunn.com/futu-api-doc/quote/update-broker.html
    def on_recv_rsp(self, rsp_pb):
        # return data: pd.DataFrame, pd.DataFrame !!! Conflict with Futu Docs
        ret_code, err_or_code, data = super(BrokerQueueHandlerImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        # data[0] 是 bid_frame_table (pandas.DataFrame), data[1] 是 ask_frame_table
        bid_df = data[0].to_dict("records")
        ask_df = data[1].to_dict("records")

        try:
            bids = parse_obj_as(list[BrokerBidEntry], bid_df)
            asks = parse_obj_as(list[BrokerAskEntry], ask_df)
        except ValidationError as err:
            logger.warning("invalid order queue record: %s", data)
            return RET_ERROR, None

        bid_dicts = [b.dict() for b in bids]
        ask_dicts = [a.dict() for a in asks]
        parsed_data = (pd.DataFrame(bid_dicts), pd.DataFrame(ask_dicts))

        try:
            # data to flat dataframe
            df = self.transformer.flattern(parsed_data)
        except Exception as e:
            logger.error("transform to flat table failed: %s", e)
            return RET_ERROR, None

        try:
            tbl = self.formatter.format(
                df,
                ktype={
                    'time': kx.TimestampVector,
                },
                time_fields=['time'],
                field_map=self.field_map
            )
        except Exception as e:
            logger.error("format to pykx table failed: %s", e)
            return RET_ERROR, None

        try:
            self.publisher.publish("FlatBrokerQs", tbl)
        except Exception as e:
            logger.error("publish table failed: %s", e)
            return RET_ERROR, None

        return RET_OK, data






