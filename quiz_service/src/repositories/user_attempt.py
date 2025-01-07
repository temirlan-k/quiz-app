from typing import List, Protocol
from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from src.models.user_attempt import UserAttempt
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.enums import LanguageCode


class IUserAttemptRepository(Protocol):

    @abstractmethod
    async def get_correct_questions(self,session_id:UUID, user_id:UUID)->List[UserAttempt]: ...

    @abstractmethod
    async def check_correct_past(self,user_id: UUID,question_id:UUID, current_session_id: UUID)-> bool: ...

    @abstractmethod
    async def create(self, attributes: dict)->UserAttempt: ...


class UserAttemptRepository:

    def __init__(self,session:AsyncSession):
        self.session = session

    async def get_correct_questions(self,session_id:UUID, user_id:UUID)->List[UserAttempt]: 
        result =  await self.session.execute(
            select(UserAttempt).distinct()
            .where(UserAttempt.session_id == session_id)
            .where(UserAttempt.user_id == user_id)
        )
        return result.scalars().all()
    
    async def check_correct_past(self,user_id: UUID,question_id:UUID, current_session_id: UUID)-> bool:
        result =  await self.session.execute(
            select(UserAttempt).distinct()
            .where(UserAttempt.user_id == user_id)
            .where(UserAttempt.question_id == question_id)
            .where(UserAttempt.session_id!=current_session_id)
            .where(UserAttempt.is_correct == True)
        )
        return result.scalars().first()

    async def create(self,attributes:dict)->UserAttempt:
        user_attempt = UserAttempt(**attributes)
        self.session.add(user_attempt)
        await self.session.flush()
        return user_attempt