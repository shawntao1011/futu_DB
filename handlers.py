import pandas as pd
from futu import StockQuoteHandlerBase, OrderBookHandlerBase, CurKlineHandlerBase, RTDataHandlerBase, TickerHandlerBase, \
    RET_OK, BrokerHandlerBase

from futu.common.pb.Qot_Common_pb2 import SubType

from models import StockQuoteModel, CurKlineModel, OrderBookModel, RTDataModel, BrokerBidEntry, BrokerAskEntry, \
    BrokerQueueModel, TickerModel


class MultiHandler(
    StockQuoteHandlerBase,
    OrderBookHandlerBase,
    CurKlineHandlerBase,
    RTDataHandlerBase,
    TickerHandlerBase,
    BrokerHandlerBase
):
    def on_recv_rsp(self, rsp_pb):
        ret, data = super().on_recv_rsp(rsp_pb)
        if ret != RET_OK:
            return ret, data

        proto = rsp_pb.head.proto_id
        if proto == SubType.QUOTE:
            self._handle_quote(data)
        elif proto == SubType.ORDER_BOOK:
            self._handle_orderbook(data)
        elif proto in (SubType.K_DAY, SubType.K_1M):
            self._handle_kline(data)
        elif proto == SubType.TICK:
            self._handle_tick(data)
        elif proto == SubType.RT_DATA:
            self._handle_rtdata(data)
        elif proto == SubType.BROKER:
            self._handle_broker(data)

        return RET_OK, data

    def _handle_quote(self, df: pd.DataFrame):
        """处理 Level-1 报价（DataFrame）"""
        for rec in df.to_dict('records'):
            q = StockQuoteModel(**rec)
            print("QUOTE →", q)

    def _handle_orderbook(self, lst: list[dict]):
        """处理盘口深度（list of dict）"""
        for item in lst:
            ob = OrderBookModel(**item)
            print("ORDER_BOOK →", ob)

    def _handle_kline(self, df: pd.DataFrame):
        """处理 K 线（DataFrame）"""
        for rec in df.to_dict('records'):
            k = CurKlineModel(**rec)
            print("KLINE →", k)

    def _handle_tick(self, lst: list[dict]):
        """处理逐笔成交（list of dict）"""
        for item in lst:
            t = TickerModel(**item)
            print("TICK →", t)

    def _handle_rtdata(self, df: pd.DataFrame):
        """处理分时图（DataFrame）"""
        for rec in df.to_dict('records'):
            r = RTDataModel(**rec)
            print("RT_DATA →", r)

    def _handle_broker(self, data: tuple[str, pd.DataFrame, pd.DataFrame]):
        """处理经纪队列（tuple: code, bid_df, ask_df）"""
        stock_code, bid_df, ask_df = data

        bids = [
            BrokerBidEntry(**row)
            for row in bid_df.to_dict('records')
        ]
        asks = [
            BrokerAskEntry(**row)
            for row in ask_df.to_dict('records')
        ]
        bq = BrokerQueueModel(
            stock_code=stock_code,
            bid_frame=bids,
            ask_frame=asks
        )
        print("BROKER_QUEUE →", bq)

