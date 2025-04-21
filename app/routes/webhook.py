from fastapi import Request, APIRouter
from app.services.trader import TraderService
from app.services.gpt import GPTService
from app.services.mailer import Mailer
from app.services.database import TradeDatabase
from app.format.tweet_request import Tweet

router = APIRouter()

gpt = GPTService()
db = TradeDatabase()
mailer = Mailer()
trader = TraderService(db=db)


@router.on_event("startup")
async def connect_ibkr_on_startup():
    await trader.ibkr.connect()


@router.post("/webhook")
async def webhook(tweet: Tweet):
    tweet = tweet.text or tweet.tweet
    if not tweet:
        return {"status": "error", "reason": "No text found"}
    classification = await gpt.analyze(tweet)
    trade_result = trader.execute_trade(classification, tweet)
    mailer.send(
        subject="Trump Tweet Triggered Trade",
        body=f"Tweet: {tweet}\n\nClassification: {classification}\n\nAction: {trade_result}")
    return {"status": "ok", "tweet": tweet, "classification": classification, "trade": trade_result}
