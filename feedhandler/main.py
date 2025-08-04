# main.py
import logging
import time
from datetime import datetime

from futu import OpenQuoteContext, RET_OK

from src.cleaners.dataframe_cleaner import DataFrameCleaner
from src.config import (
    SYMBOLS,
    SUB_TYPES,
    OPEND_HOST,
    OPEND_PORT,
    TP_HOST,
    TP_PORT,
    STP_HOST,
    STP_PORT,
    STP_USER,
    STP_PASS,
)
from src.formatters.df_to_updx_formatter import DFToUpdXFormatter
from src.handlers.broker_queue_handler import BrokerQueueHandlerImpl
from src.handlers.cur_kline_handler import CurKlineHandlerImpl
from src.handlers.order_book_handler import OrderBookHandlerImpl
from src.handlers.ticker_handler import TickerHandlerImpl
from src.publishers.archive_publisher import ArchivePublisher
from src.publishers.tp_publisher import TPPublisher
from src.transformers.broker_queue_transformer import BrokerQueueTransformer
from src.transformers.order_book_transformer import OrderBookTransformer


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)

    # 1. 建立连接，注册 Handler
    logger.info("Connecting to OpenD %s:%s", OPEND_HOST, OPEND_PORT)
    ctx = OpenQuoteContext(host=OPEND_HOST, port=OPEND_PORT)

    dataframeClearner = DataFrameCleaner()
    dfToPykxFormatter = DFToUpdXFormatter()

    # archivePublisher = ArchivePublisher(f'samples/{datetime.now().strftime("%Y%m%d")}Feed')
    logger.info("Initialising TPPublisher %s:%s", TP_HOST, TP_PORT)
    try:
        tpPublisher = TPPublisher(TP_HOST, TP_PORT)
    except Exception:
        logger.exception("Failed to initialise TPPublisher")
        return


    # order_book
    order_book = OrderBookHandlerImpl(
        transformer=OrderBookTransformer(),
        cleaner=dataframeClearner,
        formatter=dfToPykxFormatter,
        publisher=tpPublisher
    )

    # minutes
    kline = CurKlineHandlerImpl(
        transformer=None,
        cleaner=dataframeClearner,
        formatter=dfToPykxFormatter,
        publisher=tpPublisher
    )

    # ticks
    tick = TickerHandlerImpl(
        transformer=None,
        cleaner=dataframeClearner,
        formatter=dfToPykxFormatter,
        publisher=tpPublisher
    )

    # broker queue
    broker = BrokerQueueHandlerImpl(
        transformer=BrokerQueueTransformer(),
        cleaner=dataframeClearner,
        formatter=dfToPykxFormatter,
        publisher=tpPublisher
    )


    # set all callbacks
    logger.info("Registering handlers")
    ctx.set_handler(order_book)
    ctx.set_handler(kline)
    ctx.set_handler(tick)
    ctx.set_handler(broker)

    # 2. 一次性订阅所有类型
    logger.info("Subscribing to %s %s", SYMBOLS, SUB_TYPES)
    ret, err = ctx.subscribe(SYMBOLS, SUB_TYPES)
    if ret != RET_OK:
        logger.error("Subscribe failed: %s", err)
        return

    # 3. 启动接收（内部会自动 spawn 线程）
    logger.info("Subscription succeeded, starting context")
    ctx.start()

    logger.info("Running… press Ctrl+C to stop")
    try:
        while True:
            time.sleep(1)  # 每秒醒一次，可做心跳或状态打印
    except KeyboardInterrupt:
        logger.info("Interrupted, shutting down…")
    finally:
        ctx.close()
        logger.info("Context closed")

if __name__ == "__main__":
    main()
