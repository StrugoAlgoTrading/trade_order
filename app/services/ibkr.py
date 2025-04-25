from app.config.settings import CONF
from ib_insync import *
import asyncio
import logging

class IBKR:
    def __init__(self):
        self.ib = IB()
        self.contract = Stock('SPY', 'SMART', 'USD')
        self.settings = CONF

    async def connect(self):
        for attempt in range(50):
            try:
                logging.info(f"Attempt {attempt+1}: Connecting to IB Gateway at {self.settings.ib_gateway_host}:{self.settings.ib_gateway_port}")
                await self.ib.connectAsync(
                    self.settings.ib_gateway_host,
                    self.settings.ib_gateway_port,
                    clientId=self.settings.ib_client_id,
                    timeout=10
                )
                logging.info("✅ Connected successfully to IB Gateway!")
                return
            except Exception as e:
                logging.error(f"Attempt {attempt+1} failed: {e}")
                await asyncio.sleep(5)

        raise Exception("❌ Could not connect to IBKR Gateway after multiple attempts.")

    def buy(self, amount):
        self.ib.placeOrder(self.contract, MarketOrder('BUY', amount))

    def sell(self, amount):
        self.ib.placeOrder(self.contract, MarketOrder('SELL', amount))
