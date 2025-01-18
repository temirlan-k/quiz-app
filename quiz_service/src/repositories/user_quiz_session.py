from typing import List
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload,selectinload

from src.models.quiz_session import UserQuizSession
from src.models.quiz import QuizLocalization,Quiz


class UserQuizSessionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_session(
        self, user_id: UUID, session_id: UUID
    ) -> UserQuizSession | None:
        result = await self.session.execute(
            select(UserQuizSession)
            .where(UserQuizSession.user_id == user_id)
            .where(UserQuizSession.id == session_id)
        )
        return result.scalars().first()

    async def get_user_sessions(self, user_id: UUID) -> List[UserQuizSession]:
        result = await self.session.execute(
            select(UserQuizSession).where(UserQuizSession.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_id(self, session_id: UUID ) -> UserQuizSession | None:
        result = await self.session.execute(
            select(UserQuizSession)
            .options(
                joinedload(UserQuizSession.quiz)
            )
            .where(UserQuizSession.id == session_id)
        )      
        return result.scalars().first()

    async def create(self, attributes: dict) -> UserQuizSession:
        user_quiz_session = UserQuizSession(**attributes)
        self.session.add(user_quiz_session)
        await self.session.flush()
        return user_quiz_session

    async def get_percentile_rank(self, quiz_id: UUID, user_score: float) -> float:
        total_users = await self.session.execute(
            select(func.count(func.distinct(UserQuizSession.user_id))).where(
                UserQuizSession.quiz_id == quiz_id
            )
        )
        total_users = total_users.scalar() or 0

        lower_users = await self.session.execute(
            select(func.count(func.distinct(UserQuizSession.user_id))).where(
                UserQuizSession.quiz_id == quiz_id, UserQuizSession.score < user_score
            )
        )
        lower_users = lower_users.scalar() or 0

        if total_users == 0:
            return 0.0
        return (lower_users / total_users) * 100
