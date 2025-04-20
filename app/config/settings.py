from app.config.model import Settings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


@lru_cache()
def _load_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("openai_api_key", "try"),
        db_host=os.getenv("db_host", "try"),
        POSTGRES_DB=os.getenv("POSTGRES_DB", "try"),
        POSTGRES_USER=os.getenv("POSTGRES_USER", "try"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "try"),
        mail_sender=os.getenv("mail_sender", "try"),
        mail_receiver=os.getenv("mail_receiver", "try"),
        mail_password=os.getenv("mail_password", "try"),
        ib_gateway_host=os.getenv("ib_gateway_host", "ib-gateway"),
        ib_gateway_port=int(os.getenv("ib_gateway_port", 4002)),
        ib_client_id=int(os.getenv("ib_client_id", 1)),
    )


get_settings = _load_settings()
