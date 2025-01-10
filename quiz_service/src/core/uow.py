from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.question import QuestionRepository
from src.repositories.quiz import QuizRepository
from src.repositories.user_attempt import UserAttemptRepository
from src.repositories.user_quiz_session import UserQuizSessionRepository
from src.models import initialize_test_data


class UnitOfWork(AbstractAsyncContextManager):
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session = self._session_factory()
        self.quizzes_repo = QuizRepository(self.session)
        self.question_repo = QuestionRepository(self.session)
        self.user_attempt_repo = UserAttemptRepository(self.session)
        self.user_quiz_session_repo = UserQuizSessionRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def rollback(self):
        await self.session.rollback()

    async def init_test_data(self):
        await initialize_test_data(self.session)