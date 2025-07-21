from futu import StockQuoteHandlerBase, OrderBookHandlerBase, CurKlineHandlerBase, RTDataHandlerBase, TickerHandlerBase, \
    RET_OK, BrokerHandlerBase, RET_ERROR

from futu.common.pb.Qot_Common_pb2 import SubType

from models import StockQuoteModel, CurKlineModel, OrderBookModel, RTDataModel, BrokerBidEntry, BrokerAskEntry, \
    BrokerQueueModel, TickerModel


class StockQuoteHandleImpl(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(StockQuoteHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        for rec in data.to_dict('records'):
            sqm = StockQuoteModel(**rec)
            print(sqm)

        return RET_OK, data

class OrderBookHandleImpl(OrderBookHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(OrderBookHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data
        
        obm = OrderBookModel(**data)
        print(obm)

        return RET_OK, data

class CurKlineHandleImpl(CurKlineHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(CurKlineHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        for rec in data.to_dict('records'):
            ckm = CurKlineModel(**rec)
            print(ckm)

        return RET_OK, data

class RTDataHandleImpl(RTDataHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(RTDataHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        for rec in data.to_dict('records'):
            rtdm = RTDataModel(**rec)
            print(rtdm)

        return RET_OK, data

class TickerHandleImpl(TickerHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(TickerHandleImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data
        
        for rec in data.to_dict('records'):
            tm = TickerModel(**rec)
            print(tm)

        return RET_OK, data

class BrokerHandlerImpl(BrokerHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, err_or_code, data = super(BrokerHandlerImpl, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            return RET_ERROR, data

        bid_df, ask_df = data
        bids = [BrokerBidEntry(**row) for row in bid_df.to_dict('records')]
        asks = [BrokerAskEntry(**row) for row in ask_df.to_dict('records')]
        bq = BrokerQueueModel(stock_code=err_or_code, bid_frame=bids, ask_frame=asks)
        print(bq)

        return RET_OK, data
