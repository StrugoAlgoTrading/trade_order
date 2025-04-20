from app.config.settings import get_settings
from ib_insync import *


class IBKR:
    def __init__(self):
        settings = get_settings
        self.ib = IB()
        self.ib.connect(settings.ib_gateway_host, settings.ib_gateway_port, clientId=settings.ib_client_id)
        self.contract = Stock('SPY', 'SMART', 'USD')

    def buy(self):
        self.ib.placeOrder(self.contract, MarketOrder('BUY', 1))

    def sell(self):
        self.ib.placeOrder(self.contract, MarketOrder('SELL', 1))
