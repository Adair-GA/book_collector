import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

if db_url := os.getenv("DB_URL"):
    sql_async_engine = create_async_engine(db_url)
else:
    raise ValueError("DB_URL environment variable not set")


# sql_async_engine = create_async_engine("sqlite+aiosqlite:///books.db", echo=True)
# sql_async_engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/book_collector", echo=True)

session_factory = sessionmaker(sql_async_engine, expire_on_commit=False, class_=AsyncSession)

async def init_db() -> None:
    async with sql_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
