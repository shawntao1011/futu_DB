from futu import OpenQuoteContext, RET_OK


class FutuClient:
    def __init__(self, host, port):
        self.ctx = OpenQuoteContext(host=host, port=port)

    def subscribe(self, symbols, sub_types):
        ret, err = self.ctx.subscribe(symbols, sub_types)
        if ret != RET_OK:
            raise RuntimeError(f"Subscribe failed: {err}")

    def set_handler(self, handler):
        self.ctx.set_handler(handler)

    def start(self):
        self.ctx.start()

    def close(self):
        self.ctx.close()

