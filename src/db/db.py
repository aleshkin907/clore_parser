from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from configs.config import settings


POSTGRES_URL = f'postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'


engine = create_engine(POSTGRES_URL)
Session = sessionmaker(engine, expire_on_commit=False)

session = Session()


class Base(DeclarativeBase):
    pass
