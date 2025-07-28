# main.py
import time
from datetime import datetime

from futu import OpenQuoteContext, RET_OK
from src.config import SYMBOLS, SUB_TYPES, OPEND_HOST, OPEND_PORT
from src.formatters.df_to_pykx_formatter import DFToPykxFormatter
from src.formatters.dict_to_pykx_formatter import DictToPykxFormatter
from src.handlers.broker_queue_handler import BrokerQueueHandlerImpl
from src.handlers.cur_kline_handler import CurKlineHandlerImpl
from src.handlers.order_book_handler import OrderBookHandlerImpl
from src.handlers.ticker_handler import TickerHandlerImpl
from src.publishers.archive_publisher import ArchivePublisher
from src.publishers.tp_publisher import TPPublisher
from src.transformers.broker_queue_transformer import BrokerQueueTransformer
from src.transformers.order_book_transformer import OrderBookTransformer


def main():

    # 1. 建立连接，注册 Handler
    ctx = OpenQuoteContext(host=OPEND_HOST, port=OPEND_PORT)

    tpPublisher = TPPublisher()

    dictToPykxFormatter = DictToPykxFormatter()
    dfToPykxFormatter = DFToPykxFormatter()
    # archivePublisher = ArchivePublisher(f'samples/{datetime.now().strftime("%Y%m%d")}Feed')
    tpPublisher = TPPublisher(TPHOST, TPPORT)

    # order_book
    order_book = OrderBookHandlerImpl(
        transformer=OrderBookTransformer(),
        formatter=dictToPykxFormatter,
        publisher=tpPublisher
    )

    # minutes
    kline = CurKlineHandlerImpl(
        transformer=None,
        formatter=dfToPykxFormatter,
        publisher=tpPublisher
    )

    # ticks
    tick = TickerHandlerImpl(
        transformer=None,
        formatter=dfToPykxFormatter,
        publisher=tpPublisher
    )

    # broker queue
    broker = BrokerQueueHandlerImpl(
        transformer=BrokerQueueTransformer(),
        formatter=dfToPykxFormatter,
        publisher=tpPublisher
    )


    # set all callbacks
    ctx.set_handler(order_book)
    ctx.set_handler(kline)
    ctx.set_handler(tick)
    ctx.set_handler(broker)

    # 2. 一次性订阅所有类型
    ret, err = ctx.subscribe(SYMBOLS, SUB_TYPES)
    if ret != RET_OK:
        print("Subscribe failed:", err)
        return

    print("⏳ 订阅成功，开始接收推送")
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
