from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='postgres_',
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    dbname: str = Field(..., alias='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...
    # options: str = ...


pg = PostgresSettings()


class VerticaSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='vertica_',
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    host: str = ...
    port: int = ...
    user: str = ...
    password: str = ...
    database: str = ...
    tlsmode: str = ...
    autocommit: bool = ...


vt = VerticaSettings()
