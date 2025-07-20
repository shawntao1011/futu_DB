# main.py
import time
from futu import OpenQuoteContext, SubType, RET_OK
from handlers import MultiHandler

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
        SubType.K_DAY,
        SubType.K_1M,
        SubType.TICKER,
        SubType.ORDER_BOOK,
        SubType.RT_DATA,
        SubType.BROKER
    ]

    # 1. 建立连接，注册 Handler
    ctx = OpenQuoteContext(host=host, port=port)
    handler = MultiHandler()
    ctx.set_handler(handler)  # 只调用一次

    # 2. 一次性订阅所有类型
    ret, err = ctx.subscribe(symbols, sub_types)
    if ret != RET_OK:
        print("Subscribe failed:", err)
        return

    print("⏳ 订阅成功，开始接收推送，15秒后自动退出…")
    # 3. 启动接收（内部会自动 spawn 线程）
    ctx.start()

    # 4. 等待一会儿，让回调跑起来
    try:
        time.sleep(15)
    except KeyboardInterrupt:
        pass

    # 5. 关闭
    print("🛑 关闭连接")
    ctx.close()

if __name__ == "__main__":
    main()
