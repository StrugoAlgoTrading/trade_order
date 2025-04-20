from app.services.ibkr import IBKR
from datetime import datetime


class TraderService:
    def __init__(self, db):
        self.ibkr = IBKR()
        self.db = db

    def execute_trade(self, classification: str, tweet: str) -> str:
        today = datetime.today().date()

        if classification == "Good for the stock market":
            if self.db.already_bought_today(today):
                return "Trade skipped: already bought today."
            self.ibkr.buy()
            action = "BUY"
        elif classification == "Bad for the stock market":
            self.ibkr.sell()
            action = "SELL"
        else:
            action = "NONE"

        self.db.save_trade(today, classification, action, tweet)
        return f"Trade executed: {action}" if action != "NONE" else "No trade executed"
