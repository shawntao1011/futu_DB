# main.py
import time
from futu import OpenQuoteContext, SubType, RET_OK
from handlers import StockQuoteHandleImpl, OrderBookHandleImpl, CurKlineHandleImpl, RTDataHandleImpl, TickerHandleImpl, BrokerHandlerImpl


def main():
    host = '127.0.0.1'
    port = 11111
    symbols = [
        # 稳定币
        'HK.01428',  # 耀才证券金融

        # 创新药
        'HK.01530',  # 三生制药
    ]
    sub_types = [
        SubType.QUOTE,
        SubType.BROKER,
        SubType.K_1M,
        SubType.RT_DATA,
        SubType.TICKER,
        SubType.BROKER
    ]

    # 1. 建立连接，注册 Handler
    ctx = OpenQuoteContext(host=host, port=port)
    stock_quote = StockQuoteHandleImpl()
    order_book = OrderBookHandleImpl()
    kline = CurKlineHandleImpl()
    rt_data = RTDataHandleImpl()
    tick = TickerHandleImpl()
    broker = BrokerHandlerImpl()

    ctx.set_handler(stock_quote)
    ctx.set_handler(order_book)
    ctx.set_handler(kline)
    ctx.set_handler(rt_data)
    ctx.set_handler(tick)
    ctx.set_handler(broker)

    # 2. 一次性订阅所有类型
    ret, err = ctx.subscribe(symbols, sub_types)
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
