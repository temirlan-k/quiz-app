from abc import ABC, abstractmethod
from typing import List, Protocol
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.question import Question, QuestionLocalization


class QuestionRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Question | None:
        result = await self.session.get(Question, id)
        return result

    async def get_list_by_quiz_id(
        self, quiz_id: UUID, language
    ) -> List[QuestionLocalization]:
        result = await self.session.execute(
            select(QuestionLocalization)
            .join(Question, QuestionLocalization.question_id == Question.id)
            .where(Question.quiz_id == quiz_id)
            .where(QuestionLocalization.language == language)
            .options(joinedload(QuestionLocalization.question))
        )

        return result.scalars().all()

    async def get_localized_question(
        self, question_id: UUID, language_code: str
    ) -> QuestionLocalization | None:
        result = await self.session.execute(
            select(QuestionLocalization)
            .join(Question, QuestionLocalization.question_id == Question.id)
            .where(Question.id == question_id)
            .where(QuestionLocalization.language == language_code)
            .options(joinedload(QuestionLocalization.question))
        )
        return result.scalars().first()

    async def create_question(self, attributes: dict) -> Question:
        question = Question(**attributes)
        self.session.add(question)
        await self.session.flush()
        return question

    async def create_question_localization(
        self, attributes: dict
    ) -> QuestionLocalization:
        question_loc = QuestionLocalization(**attributes)
        self.session.add(question_loc)
        await self.session.flush()
        return question_loc

    async def count_questions(self, quiz_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(Question)
            .where(Question.quiz_id == quiz_id)
        )
        return result.scalar_one() or 0
