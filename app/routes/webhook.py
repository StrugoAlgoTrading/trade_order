from fastapi import Request, APIRouter
from app.services.trader import TraderService
from app.services.gpt import GPTService
from app.services.mailer import Mailer
from app.services.database import TradeDatabase
from app.format.event import Event

router = APIRouter()

db = TradeDatabase()
mailer = Mailer()
trader = TraderService(db="db")


@router.on_event("startup")
async def connect_ibkr_on_startup():
    await trader.ibkr.connect()


@router.post("/webhook")
async def webhook(event: Event):
    print(event)
    trade_result = trader.execute_trade(event)
    db.save_trade(order, event.event_type, event.time, event.ticker, action, event.context, trade_time,
                       trade_price,
                       position)
    # mailer.send(
    #     subject="Trump Tweet Triggered Trade",
    #     body=f"Tweet: {tweet}\n\nClassification: {classification}\n\nAction: {trade_result}")
    # return {"status": "ok", "tweet": tweet, "classification": classification, "trade": trade_result}
