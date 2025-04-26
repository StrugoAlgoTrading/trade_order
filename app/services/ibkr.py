from app.config.settings import CONF
from ib_insync import *
import asyncio
import logging
import socket

class IBKR:
    def __init__(self):
        self.ib = IB()
        self.contract = Stock('SPY', 'SMART', 'USD')
        self.settings = CONF

    async def connect(self):
        max_attempts = 50
        delay_between_attempts = 10 # seconds

        for attempt in range(1, max_attempts + 1):
            try:
                print(f"🟢 Attempt {attempt}: trying to connect to IB Gateway...")
                await self.ib.connectAsync(
                    self.settings.ib_gateway_host,
                    self.settings.ib_gateway_port,
                    clientId=self.settings.ib_client_id,
                    timeout=60
                )
                print("✅ Connected successfully to IB Gateway!")
                return

            except Exception as e:
                print(f"⚠️ Attempt {attempt} failed to connect: {e}")
                await asyncio.sleep(delay_between_attempts)

        raise Exception("❌ Could not connect to IBKR Gateway after multiple attempts.")

    def is_port_open(self, host, port):
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"🔵 Port {port} on {host} is open.")
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            print(f"🔴 Port {port} on {host} is not open.")
            return False

    def buy(self, amount):
        self.ib.placeOrder(self.contract, MarketOrder('BUY', amount))

    def sell(self, amount):
        self.ib.placeOrder(self.contract, MarketOrder('SELL', amount))
