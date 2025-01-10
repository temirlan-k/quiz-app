from typing import Protocol
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.balance import Balance


class IBalanceRepository(Protocol):
    async def get_balance(self, user_id: UUID) -> Balance: ...
    async def update_balance(self, user_id: UUID, new_balance: float) -> None: ...
    async def create(self, attributes: dict) -> Balance: ...


class BalanceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_balance(self, user_id: UUID) -> Balance | None:
        try:
            result = await self.session.execute(
                select(Balance).where(Balance.user_id == user_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            print(f"Database error in get_balance: {e}")
            raise

    async def create(self, attributes: dict) -> Balance:
        try:
            balance = Balance(**attributes)
            self.session.add(balance)
            return balance
        except SQLAlchemyError as e:
            print(f"Database error in create: {e}")
            raise

    async def update_balance(self, user_id: UUID, new_balance: float) -> None:
        try:
            await self.session.execute(
                update(Balance)
                .values(balance=new_balance)
                .where(Balance.user_id == user_id)
            )
        except SQLAlchemyError as e:
            print(f"Database error in update_balance: {e}")
            raise e
