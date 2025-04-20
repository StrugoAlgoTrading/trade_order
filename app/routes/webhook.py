from fastapi import APIRouter, Request
from app.services.trader import TraderService
from app.services.gpt import GPTService
from app.services.mailer import Mailer
from app.services.database import TradeDatabase

router = APIRouter()
gpt = GPTService()
db = TradeDatabase()
mailer = Mailer()
trader = TraderService(db=db)


@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    tweet = data.get("text") or data.get("tweet")
    if not tweet:
        return {"status": "error", "reason": "No text found"}

    classification = await gpt.analyze(tweet)
    trade_result = trader.execute_trade(classification, tweet)
    mailer.send(
        subject="Trump Tweet Triggered Trade",
        body=f"Tweet: {tweet}\n\nClassification: {classification}\n\nAction: {trade_result}"
    )

    return {
        "status": "ok",
        "tweet": tweet,
        "classification": classification,
        "trade": trade_result
    }
