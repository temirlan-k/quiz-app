import os

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Quiz App"
    debug: bool = Field(default=True, env="DEBUG")
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASS: str = "guest"
    RABBITMQ_VHOST: str = "/"

    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"

    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")

    @property
    def async_db_url(self) -> str:
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", 5432)
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        print(
            f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        return f"postgresql+asyncpg://balance_user:balance_password@balance_db:5432/balance_db"

    @property
    def sync_db_url(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql",
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=str(self.db_port),
            path=f"/{self.db_name}",
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

print("Async DB URL:", settings.async_db_url)
print("Debug Mode:", settings.debug)
