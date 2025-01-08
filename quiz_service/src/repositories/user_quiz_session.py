from typing import List, Protocol
from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from src.models.quiz_session import UserQuizSession
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.enums import LanguageCode


class IUserQuizSessionRepository(Protocol):

    @abstractmethod
    async def get_user_sessions(self,user_id: UUID)->UserQuizSession | None: ...

    @abstractmethod
    async def get_by_id(self,session_id)->UserQuizSession | None: ...

    @abstractmethod
    async def create(self,attributes: dict)->UserQuizSession: ...


class UserQuizSessionRepository(IUserQuizSessionRepository):

    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_user_session(self, user_id: UUID, session_id: UUID)->UserQuizSession|None:
        result = await self.session.execute(
            select(UserQuizSession).where(UserQuizSession.user_id == user_id).where(UserQuizSession.id == session_id)
        )
        return result.scalars().first()

    async def get_user_sessions(self, user_id:UUID)-> List[UserQuizSession]:
        result = await self.session.execute(
            select(UserQuizSession).where(UserQuizSession.user_id == user_id)
        )
        return result.scalars().all()
    
    async def get_by_id(self, session_id:UUID)->UserQuizSession|None:
        result = await self.session.execute(
            select(UserQuizSession).where(UserQuizSession.id == session_id)
        )
        return result.scalars().first()


    async def create(self, attributes:dict)->UserQuizSession:
        user_quiz_session = UserQuizSession(**attributes)
        self.session.add(user_quiz_session)
        await self.session.flush()
        return user_quiz_session

