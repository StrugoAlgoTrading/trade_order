from app.config.settings import get_settings
from ib_insync import *


class IBKR:
    def __init__(self):
        self.ib = IB()
        self.contract = Stock('SPY', 'SMART', 'USD')
        self.settings = get_settings

    async def connect(self):
        await self.ib.connectAsync(
            self.settings.ib_gateway_host,
            self.settings.ib_gateway_port,
            clientId=self.settings.ib_client_id
        )

    def buy(self):
        self.ib.placeOrder(self.contract, MarketOrder('BUY', 1))

    def sell(self):
        self.ib.placeOrder(self.contract, MarketOrder('SELL', 1))
