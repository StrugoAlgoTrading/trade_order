from .ibkr import IBKR
from datetime import datetime
from ..format.event import Event
import asyncio
import datetime
from ib_insync import Stock, MarketOrder
from typing import Tuple


class TraderService(IBKR):
    def __init__(self):
        IBKR.__init__(self)
        self.amount = 10

    async def trade(self, event):
        contract = Stock(event.ticker, 'SMART', 'USD')
        tracking_start_time = datetime.datetime.utcnow()
        event_price = self.get_event_price(event.ticker, event.time)
        live_ticker = self.ib.reqMktData(contract, '', False, False)
        entry = self.open_position(event_price, tracking_start_time, live_ticker, contract)
        if entry:
            all_positions = self.flip_position(entry, tracking_start_time, live_ticker, event_price, contract)
        return all_positions

    async def open_position(self, event_price, tracking_start_time, live_ticker, contract):
        upper, lower = event_price * 1.003, event_price * 0.997
        entry = None
        while (datetime.datetime.utcnow() - tracking_start_time).total_seconds() < 600:
            price = live_ticker.last or live_ticker.close
            if price >= upper:
                fill_price, fill_time = await self.enter_position(contract, 'BUY', self.amount)
                entry = [{'position_side': 'long', 'price': fill_price, 'time': fill_time}]
                break
            if price <= lower:
                fill_price, fill_time = await self.enter_position(contract, 'SELL', self.amount)
                entry = [{'position_side': 'short', 'price': fill_price, 'time': fill_time}]
                break
            await asyncio.sleep(1)
        return entry

    async def flip_position(self, entry, tracking_start_time, live_ticker, event_price, contract):
        position_side = entry[-1]['position_side']
        while (datetime.datetime.utcnow() - tracking_start_time).total_seconds() < 600:
            price = live_ticker.last or live_ticker.close

            if position_side == 'long' and price <= event_price:
                fill_price, fill_time = await self.enter_position(contract, 'SELL', self.amount)
                entry.append({'type': 'short', 'price': fill_price, 'time': fill_time})
                position_side = 'short'
                print(f"❗ הפכתי לפוזיציית שורט ב־{price:.2f}")

            elif position_side == 'short' and price >= event_price:
                fill_price, fill_time = await self.enter_position(contract, 'BUY', self.amount)
                entry.append({'type': 'long', 'price': fill_price, 'time': fill_time})
                position_side = 'long'
                print(f"❗ הפכתי לפוזיציית לונג ב־{price:.2f}")

            await asyncio.sleep(1)
        return entry
    
    def get_event_price(self, stock: Stock, at_time: datetime.datetime) -> float:
        start = at_time.strftime("%Y%m%d %H:%M:%S")
        end = (at_time + datetime.timedelta(seconds=1)).strftime("%Y%m%d %H:%M:%S")
        ticks = self.ib.reqHistoricalTicks(
            stock,
            startDateTime=start,
            endDateTime=end,
            numberOfTicks=1,
            whatToShow='TRADES',
            useRth=False
        )
        return float(ticks[0].price)

    async def enter_position(self, contract, action: str, amount: int) -> Tuple[float, str]:
        order = MarketOrder(action, amount)
        trade = self.ib.placeOrder(contract, order)
        while trade.orderStatus.status != 'Filled':
            await asyncio.sleep(0.1)
        fill_price = trade.fills[-1].execution.price
        fill_time = trade.fills[-1].execution.time
        return fill_price, fill_time
