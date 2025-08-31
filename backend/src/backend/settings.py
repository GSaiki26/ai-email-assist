from pydantic import AmqpDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AMQPSettings(BaseSettings):
    dsn: AmqpDsn
    queue_name: str


class DatabaseSettings(BaseSettings):
    dsn: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    ai_processor_amqp: AMQPSettings = Field(default=...)
    database: DatabaseSettings = Field(default=...)
