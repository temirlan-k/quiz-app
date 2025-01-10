from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import async_session_factory
from src.repositories.balance import BalanceRepository


class UnitOfWork(AbstractAsyncContextManager):
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._registry_repository = {}

    async def __aenter__(self):
        self.session = self._session_factory()
        self.balance_repo = BalanceRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                await self.rollback()
            await self.session.close()

    async def commit(self):
            await self.session.commit()

    async def rollback(self):
            await self.session.rollback()
