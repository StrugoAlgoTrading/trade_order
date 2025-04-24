from app.config.settings import get_settings
from ib_insync import *
from time import sleep

class IBKR:
    def __init__(self):
        self.ib = IB()
        self.contract = Stock('SPY', 'SMART', 'USD')
        self.settings = get_settings

    async def connect(self):
        for attempt in range(15):
            try:
                await self.ib.connectAsync(
                    self.settings.ib_gateway_host,
                    self.settings.ib_gateway_port,
                    clientId=self.settings.ib_client_id
                )
                return
            except:
                sleep(5)

    def buy(self, stocks_count):
        self.ib.placeOrder(self.contract, MarketOrder('BUY', stocks_count))

    def sell(self, stocks_count):
        self.ib.placeOrder(self.contract, MarketOrder('SELL', stocks_count))
