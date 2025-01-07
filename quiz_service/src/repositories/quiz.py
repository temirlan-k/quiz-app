
from typing import List, Protocol
from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from src.models.quiz import Quiz,QuizLocalization
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.enums import LanguageCode


class IQuizRepository(Protocol):

    @abstractmethod
    async def get_by_id(self, id: UUID)-> Quiz | None: ...

    @abstractmethod
    async def get_all(self,)-> List[Quiz]: ...

    @abstractmethod
    async def create_quiz(self,)-> Quiz: ...

    @abstractmethod
    async def create_quiz_localization(self, attributes: dict)-> QuizLocalization: ...


class QuizRepository(IQuizRepository):

    def __init__(self, session: AsyncSession)-> None:
        self.session = session
    
    async def get_by_id(self, id: UUID)-> Quiz | None:
        result = await self.session.get(Quiz,id)
        return result
    
    async def get_all(self,language_code:str,offset: int = 0, limit:int =10,)-> List[Quiz]:
        result = await self.session.execute(
            select(QuizLocalization)
            .where(QuizLocalization.language == language_code)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_quiz(self,)-> Quiz | None:
        quiz = Quiz()
        self.session.add(quiz)
        await self.session.flush()
        return quiz

    async def create_quiz_localization(self,attributes: dict)-> QuizLocalization | None:
        quiz_localization = QuizLocalization(**attributes)
        self.session.add(quiz_localization)
        await self.session.flush()
        return quiz_localization