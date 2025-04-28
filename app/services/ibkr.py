from app.config.settings import CONF
from ib_insync import IB

import asyncio
import logging
import socket


class IBKR:
    def __init__(self):
        self.ib = IB()
        self.settings = CONF

    async def connect(self):
        for attempt in range(1, 50):
            try:
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
                await asyncio.sleep(10)
        raise Exception("❌ Could not connect to IBKR Gateway after multiple attempts.")


