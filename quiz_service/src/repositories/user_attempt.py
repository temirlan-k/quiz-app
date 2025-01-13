from typing import List
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_attempt import UserAttempt


class UserAttemptRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_correct_questions_(
        self, session_id: UUID, user_id: UUID
    ) -> List[UserAttempt]:
        result = await self.session.execute(
            select(UserAttempt).where(
                and_(
                    UserAttempt.user_id == user_id,
                    UserAttempt.session_id != session_id,
                    UserAttempt.is_correct == True,
                )
            )
        )
        return result.scalars().all()

    async def check_correct_past(
        self, user_id: UUID, question_id: UUID, current_session_id: UUID
    ) -> bool:
        result = await self.session.execute(
            select(UserAttempt).where(
                and_(
                    UserAttempt.user_id == user_id,
                    UserAttempt.question_id == question_id,
                    UserAttempt.session_id != current_session_id,
                    UserAttempt.is_correct == True,
                )
            )
        )
        return result.scalars().first() is not None

    async def create(self, attributes: dict) -> UserAttempt:
        user_attempt = UserAttempt(**attributes)
        self.session.add(user_attempt)
        await self.session.flush()
        return user_attempt

    async def get_by_user_question_session(
        self,
        user_id: UUID,
        question_id: UUID,
        session_id: UUID,
    ):
        result = await self.session.execute(
            select(UserAttempt).where(
                and_(
                    UserAttempt.user_id == user_id,
                    UserAttempt.question_id == question_id,
                    UserAttempt.session_id == session_id,
                )
            )
        )
        return result.scalars().first()

    async def get_correct_attempts_in_session(
        self, session_id: UUID, user_id: UUID
    ) -> List[UserAttempt]:
        result = await self.session.execute(
            select(UserAttempt).where(
                and_(
                    UserAttempt.user_id == user_id,
                    UserAttempt.session_id == session_id,
                    UserAttempt.is_correct == True,
                )
            )
        )
        return result.scalars().all()
