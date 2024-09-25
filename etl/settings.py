from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='kafka_'
    )
    topics: str = ...
    bootstrap_servers: str = ...
    auto_offset_reset: str = Field(..., alias='KAFKA_OFFSET_RESET')
    consumer_timeout_ms: int = Field(..., alias='KAFKA_TIMEOUT')
    group_id: str = ...
    max_poll_records: int = Field(..., alias='KAFKA_MAX_POLL')
    enable_auto_commit: bool = Field(..., alias='KAFKA_COMMIT')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
    clickhouse_host: str = ...
    cluster: str = ...
    database: str = ...
    table: str = ...


kafka_settings = KafkaSettings()
settings = Settings()
