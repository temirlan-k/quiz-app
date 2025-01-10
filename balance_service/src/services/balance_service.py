from uuid import UUID

from src.core.uow import UnitOfWork
from src.core.exceptions.base import BadRequestException


class BalanceService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def my_balance(self,user_id:UUID,):
        async with self._uow as uow:
            try:
                user_balance = await uow.balance_repo.get_balance(user_id)
                if user_balance is None :
                    raise BadRequestException("User balance not found")
                return user_balance
            except Exception as e:
                raise e

    async def process_quiz_completion(self, user_id: UUID, correct_count: int, current_streak:int) -> None:
        base_point = correct_count * 100
        
        if current_streak > 0:
            streak_bonus = base_point * (1 + (current_streak - 1) * 0.1)
        else:
            streak_bonus = 0 
        
        total_points = base_point + streak_bonus
        await self.award_balance(user_id, total_points)

    async def award_balance(self, user_id: UUID, amount: float) -> None:
        async with self._uow as uow:
            try:
                balance = await uow.balance_repo.get_balance(user_id)

                if balance is None:
                    await uow.balance_repo.create(
                        {"user_id": user_id, "balance": amount}
                    )
                else:
                    new_balance = float(balance.balance) + float(amount)
                    await uow.balance_repo.update_balance(user_id, new_balance)

                await uow.commit()
            except Exception as e:
                raise e
