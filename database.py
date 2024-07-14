from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
