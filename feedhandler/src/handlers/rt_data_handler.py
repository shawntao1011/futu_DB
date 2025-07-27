import logging
import os
import pickle
from datetime import datetime

from futu import RTDataHandlerBase, RET_OK, RET_ERROR

from feedhandler.src.models.rt_data_model import RTDataModel
from feedhandler.src.publishers.tp_publisher import TPPublisher

logger = logging.getLogger(__name__)

class RTDataHandleImpl(RTDataHandlerBase):
    def __init__(self, publisher: TPPublisher, sample_dir = r"samples/rtdata") -> None:
        super().__init__()
        self.publisher = publisher
        self.sample_dir = sample_dir
        os.makedirs(self.sample_dir, exist_ok=True)

        self.buffer: list[RTDataModel] = []
        self.current_minute: str = ""

    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(RTDataHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        for rec in data.to_dict('records'):
            from pydantic import ValidationError
            try:
                rtdm = RTDataModel(**rec)
            except ValidationError as err:
                logger.warning("invalid real time record: %s", rec)
            self._buffer_and_maybe_flush(rtdm)

        return RET_OK, data

    def _buffer_and_maybe_flush(self, dm):
        now = datetime.now()
        minute_key = now.strftime("%Y%m%dT%H%M")

        if self.current_minute == "":
            self.current_minute = minute_key

        if minute_key != self.current_minute:
            self._flush_to_pickle()
            self.buffer = []
            self.current_minute = minute_key

        self.buffer.append(dm)

    def _flush_to_pickle(self):
        if not self.buffer:
            return

        filename = f"{self.current_minute}.pkl"
        filepath = os.path.join(self.sample_dir, filename)
        with open(filepath, "wb") as f:
            pickle.dump(self.buffer, f)
        logger.info("flushed %d records to %s", len(self.buffer), filepath)