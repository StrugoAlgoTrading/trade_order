from app.config.settings import CONF
import psycopg2


class TradeDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=CONF.db_host,
            database=CONF.POSTGRES_DB,
            user=CONF.POSTGRES_USER,
            password=CONF.POSTGRES_PASSWORD
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            classification TEXT,
            action TEXT,
            tweet TEXT,
            trade_time DATE NOT NULL
        )
        """)

    def already_bought_today(self, today):
        self.cur.execute("SELECT COUNT(*) FROM trades WHERE date = %s AND action = 'BUY'", (today,))
        return self.cur.fetchone()[0] > 0

    def save_trade(self, date, classification, action, tweet, trade_time):
        self.cur.execute(
            "INSERT INTO trades (date, classification, action, tweet, trade_time) VALUES (%s, %s, %s, %s, %s)",
            (date, classification, action, tweet, trade_time)
        )
