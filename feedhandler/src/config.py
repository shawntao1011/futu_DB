# config.py
from futu import SubType

# OpenD 配置
OPEND_HOST = '127.0.0.1'
OPEND_PORT = 11111

# 订阅合约
SYMBOLS = [
    # 稳定币
    'HK.01428', # 耀才证券金融
    'HK.01788', # 国泰君安国际

    # 创新药
    'HK.01530', # 三生制药
    'HK.01177', # 中国生物制药
]

SUB_TYPES: list[str] = [
    SubType.K_1M,
    SubType.TICKER,
    SubType.ORDER_BOOK,
    SubType.BROKER,
]

# TickerPlant 配置
TP_HOST = '127.0.0.1'
TP_PORT = 5010

# TorQ 配置
STP_HOST = '127.0.0.1'
STP_PORT = 6000
STP_USER = 'feed'
STP_PASS = 'pass'