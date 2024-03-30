from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from configs.config import settings
from sqlalchemy.orm import Session


POSTGRES_URL = f'postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'


engine = create_engine(POSTGRES_URL)
Session = sessionmaker(engine, expire_on_commit=False)

session = Session()

# session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db_connection():
#     db = scoped_session(session_local)
#     try:
#         yield db
#     finally:
#         db.close()


class Base(DeclarativeBase):
    pass


# class PostgesDB:
#     session: Session


#     def __init__(self) -> None:
#         engine = create_engine(POSTGRES_URL)
#         Session = sessionmaker(engine, expire_on_commit=False)


#         self.session = Session()

# engine = create_async_engine(POSTGRES_URL)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# class Base(DeclarativeBase):
#     pass


# async def get_async_session():
#     async with async_session_maker() as session:
#         yield session


# POSTGRES_URL = f'postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
# engine = create_engine(POSTGRES_URL)
# Session = sessionmaker(engine, expire_on_commit=False)
# session = Session()


# class Base(DeclarativeBase):
#     pass
