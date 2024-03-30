from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: Optional[str] = "localhost"
    DB_PORT: Optional[int] = 5432
    DB_USER: Optional[str] = "postgres"
    DB_PASS: Optional[str] = "postgres"
    DB_NAME: Optional[str] = "postgres"

    REDIS_HOST: Optional[str] = "localhost"
    REDIS_PORT: Optional[int] = 228
    REDIS_DB: Optional[int] = 0

    SECRET_KEY: Optional[str] = "YOUR SECRET KEY"


    class Config:
        env_file = ".env"

settings = Settings()
