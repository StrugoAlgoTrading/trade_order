from app.config.model import Settings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


@lru_cache()
def _load_settings() -> Settings:
    return Settings(
        db_host=os.getenv("db_host"),
        POSTGRES_DB=os.getenv("POSTGRES_DB"),
        POSTGRES_USER=os.getenv("POSTGRES_USER"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
        mail_sender=os.getenv("mail_sender"),
        mail_receiver=os.getenv("mail_receiver"),
        mail_password=os.getenv("mail_password"),
        ib_gateway_host=os.getenv("ib_gateway_host"),
        ib_gateway_port=int(os.getenv("ib_gateway_port")),
        ib_client_id=int(os.getenv("ib_client_id")),
    )


get_settings = _load_settings()
