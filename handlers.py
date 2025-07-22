import os
import pickle
from datetime import datetime

from futu import (
    StockQuoteHandlerBase,
    OrderBookHandlerBase,
    CurKlineHandlerBase,
    RTDataHandlerBase,
    TickerHandlerBase,
    RET_OK,
    BrokerHandlerBase,
    RET_ERROR
)

import logging

from pydantic import ValidationError

from feedTo.tp_publisher import TPPublisher
from models import (
    StockQuoteModel,
    CurKlineModel,
    OrderBookModel,
    RTDataModel,
    BrokerBidEntry,
    BrokerAskEntry,
    BrokerQueueModel,
    TickerModel
)

logger = logging.getLogger(__name__)

class StockQuoteHandleImpl(StockQuoteHandlerBase):
    def __init__(self, publisher: TPPublisher, sample_dir = r"samples/stockquote") -> None:
        super().__init__()
        self.publisher = publisher
        self.sample_dir = sample_dir
        os.makedirs(self.sample_dir, exist_ok=True)

        self.buffer: list[StockQuoteModel] = []
        self.current_minute: str = ""

    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(StockQuoteHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        for rec in data.to_dict('records'):
            try:
                sqm = StockQuoteModel(**rec)
                print(sqm)
                self._buffer_and_maybe_flush(sqm)
            except ValidationError as exc:
                logger.warning("invalid stock quote record: %s", rec)
                continue

            #self.publisher.publish

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


class OrderBookHandleImpl(OrderBookHandlerBase):
    def __init__(self, publisher: TPPublisher, sample_dir = r"samples/orderbook") -> None:
        super().__init__()
        self.publisher = publisher
        self.sample_dir = sample_dir
        os.makedirs(self.sample_dir, exist_ok=True)

        self.buffer: list[OrderBookModel] = []
        self.current_minute: str = ""

    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(OrderBookHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data
        
        obm = OrderBookModel(**data)
        print(obm)
        self._buffer_and_maybe_flush(obm)

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

class CurKlineHandleImpl(CurKlineHandlerBase):
    def __init__(self, publisher: TPPublisher, sample_dir = r"samples/curkline") -> None:
        super().__init__()
        self.publisher = publisher
        self.sample_dir = sample_dir
        os.makedirs(self.sample_dir, exist_ok=True)

        self.buffer: list[CurKlineModel] = []
        self.current_minute: str = ""

    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(CurKlineHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        for rec in data.to_dict('records'):
            ckm = CurKlineModel(**rec)
            print(ckm)
            self._buffer_and_maybe_flush(ckm)

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
            rtdm = RTDataModel(**rec)
            print(rtdm)
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



class TickerHandleImpl(TickerHandlerBase):
    def __init__(self, publisher: TPPublisher, sample_dir = r"samples/ticker") -> None:
        super().__init__()
        self.publisher = publisher
        self.sample_dir = sample_dir
        os.makedirs(self.sample_dir, exist_ok=True)

        self.buffer: list[TickerModel] = []
        self.current_minute: str = ""

    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(TickerHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data
        
        for rec in data.to_dict('records'):
            tm = TickerModel(**rec)
            print(tm)
            self._buffer_and_maybe_flush(tm)

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

class BrokerHandlerImpl(BrokerHandlerBase):
    def __init__(self, publisher: TPPublisher, sample_dir = r"samples/broker") -> None:
        super().__init__()
        self.publisher = publisher
        self.sample_dir = sample_dir
        os.makedirs(self.sample_dir, exist_ok=True)

        self.buffer: list[BrokerQueueModel] = []
        self.current_minute: str = ""

    def on_recv_rsp(self, rsp_pb):
        ret_code, err_or_code, data = super(BrokerHandlerImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        bid_df, ask_df = data
        bids = [BrokerBidEntry(**row) for row in bid_df.to_dict('records')]
        asks = [BrokerAskEntry(**row) for row in ask_df.to_dict('records')]
        bqm = BrokerQueueModel(stock_code=err_or_code, bid_frame=bids, ask_frame=asks)
        print(bqm)
        self._buffer_and_maybe_flush(bqm)

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