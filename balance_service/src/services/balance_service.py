from uuid import UUID
from src.core.uow import UnitOfWork

class BalanceService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def process_quiz_completion(self, user_id: UUID, correct_count: int) -> None:
        points = correct_count  + 1000
        await self.award_balance(user_id, points)

    async def award_balance(self, user_id: UUID, amount: float) -> None:
        async with self._uow as uow:
            try:
                balance = await uow.balance_repo.get_balance(user_id)
                
                if balance is None:
                    await uow.balance_repo.create({
                        "user_id": user_id,
                        "balance": amount
                    })
                else:
                    new_balance = balance.balance + amount
                    await uow.balance_repo.update_balance(user_id, new_balance)

                await uow.commit()
                return new_balance
            except Exception as e:
                await uow.rollback()
                raise
