from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

sql_async_engine = create_async_engine("sqlite+aiosqlite:///books.db", echo=True)

session_factory = sessionmaker(sql_async_engine, expire_on_commit=False, class_=AsyncSession)

async def init_db() -> None:
    async with sql_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
