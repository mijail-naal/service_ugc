from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='src/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    secret_key: str = ...
    jwt_secret_key: str = ...
    kafka_host: str = ...
    kafka_port: int = ...


settings = Settings()


class DefaultTopic(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='src/.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='topic_'
    )
    name: str = ...
    partition: int = ...
    replication: int = ...
    min_insync: int = ...
    retention: int = ...


defaul_topic = DefaultTopic()
