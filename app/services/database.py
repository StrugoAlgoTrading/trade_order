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
            event_type TEXT,
            event_time DATE NOT NULL,
            ticker TEXT,
            action TEXT,
            context TEXT,
            trade_time DATE NOT NULL
        )
        """)

    def save_trade(self, event_type, event_time, ticker, action, context, trade_time):
        self.cur.execute(
            "INSERT INTO trades "
            "(event_type, event_time, ticker, action, context, trade_time) VALUES (%s, %s, %s, %s, %s, %s)",
            (event_type, event_time, ticker, action, context, trade_time)
        )
