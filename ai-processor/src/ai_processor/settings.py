from pydantic import AmqpDsn, Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AMQPSettings(BaseSettings):
    dsn: AmqpDsn
    queue_name: str


class DatabaseSettings(BaseSettings):
    dsn: str


class HTTPSettings(BaseSettings):
    base_url: HttpUrl
    concurrency: int = Field(default=1)
    timeout_secs: float = Field(default=10.0)
    cooldown_secs: float = Field(default=0.0)


class OpenAISettings(HTTPSettings):
    api_key: SecretStr
    model: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    ai_processor_amqp: AMQPSettings = Field(default=...)
    database: DatabaseSettings = Field(default=...)

    openai: OpenAISettings = Field(default=...)
