# main.py
import time
from futu import OpenQuoteContext, RET_OK
from config import SYMBOLS, SUB_TYPES, OPEND_HOST, OPEND_PORT
from feedTo.tp_publisher import TPPublisher
from handlers import StockQuoteHandleImpl, OrderBookHandleImpl, CurKlineHandleImpl, RTDataHandleImpl, TickerHandleImpl, BrokerHandlerImpl


def main():

    # 1. 建立连接，注册 Handler
    ctx = OpenQuoteContext(host=OPEND_HOST, port=OPEND_PORT)

    publisher = TPPublisher()

    stock_quote = StockQuoteHandleImpl(publisher)
    order_book = OrderBookHandleImpl(publisher)
    kline = CurKlineHandleImpl(publisher)
    rt_data = RTDataHandleImpl(publisher)
    tick = TickerHandleImpl(publisher)
    broker = BrokerHandlerImpl(publisher)

    ctx.set_handler(stock_quote)
    ctx.set_handler(order_book)
    ctx.set_handler(kline)
    ctx.set_handler(rt_data)
    ctx.set_handler(tick)
    ctx.set_handler(broker)

    # 2. 一次性订阅所有类型
    ret, err = ctx.subscribe(SYMBOLS, SUB_TYPES)
    if ret != RET_OK:
        print("Subscribe failed:", err)
        return

    print("⏳ 订阅成功，开始接收推送，15秒后自动退出…")
    # 3. 启动接收（内部会自动 spawn 线程）
    ctx.start()

    print("▶️ 运行中…按 Ctrl+C 停止")
    try:
        while True:
            time.sleep(1)  # 每秒醒一次，可做心跳或状态打印
    except KeyboardInterrupt:
        print("🛑 程序中断，正在关闭…")
    finally:
        ctx.close()

if __name__ == "__main__":
    main()
