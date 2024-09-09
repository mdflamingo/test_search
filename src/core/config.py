import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    postgres_db: str = Field('posts', alias='POSTGRES_DB')
    postgres_port: int = Field(5432, alias='DB_PORT')
    postgres_host: str = Field('127.0.0.1', alias='DB_HOST')
    postgres_user: str = Field('postgres', alias='POSTGRES_USER')
    postgres_password: str = Field('123qwe', alias='POSTGRES_PASSWORD')

    es_host: str = Field('elasticsearch', alias='ES_HOST')
    es_port: int = Field('9200', alias='ES_PORT')
    index_name: str = Field('posts', alias='INDEX_NAME')

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '.env'),
        env_file_encoding='utf-8')


settings = Settings()
