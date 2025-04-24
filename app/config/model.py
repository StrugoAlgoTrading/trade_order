from pydantic import BaseModel


class Settings(BaseModel):
    db_host: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    mail_sender: str
    mail_receiver: str
    mail_password: str
    ib_gateway_host: str
    ib_gateway_port: int
    ib_client_id: int
