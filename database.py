from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from decouple import config
from typing import TypeAlias, Annotated
from collections.abc import AsyncGenerator

db_name = config("DB_NAME")
db_user = config("DB_USER")
db_password = config("DB_PASSWORD")
db_host = config("DB_HOST")
db_port = config("DB_PORT")

url = "postgresql+asyncpg://%s:%s@%s:%s/%s" % (db_user, db_password, db_host, db_port, db_name)

engine = create_async_engine(url, pool_pre_ping=True, pool_size=10, max_overflow=20)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

DB_DEP: TypeAlias = Annotated[AsyncSession, Depends(get_db)]
