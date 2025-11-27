from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from app.db.base import Base
from app.config import get_database_logger
from app.config import config

logger = get_database_logger()


class Database:
    def __init__(self):
        self.engine = None
        self.async_session = None
        self.logger = logger

    async def init(self):
        self.logger.info(f"Initializing database: {config.database.url}")

        self.engine = create_async_engine(
            config.database.url,
            echo=False,
            future=True,
        )

        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        # async with self.engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.create_all)

        self.logger.info("Database initialized successfully")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self.async_session:
            raise RuntimeError("Database not initialized")

        session = self.async_session()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self):
        if self.engine:
            await self.engine.dispose()
            self.logger.info("Database connections closed")


db = Database()
