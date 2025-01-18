from typing import Dict

from src.core.enums import LanguageCode
from src.core.uow import UnitOfWork


class QuizService:

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def create_quiz(self, quiz_data: Dict[list, dict]) -> dict:
        async with self._uow as uow:
            try:
                quiz = await self._uow.quizzes_repo.create_quiz()
                for loc in quiz_data.get("localizations"):
                    quiz_loc = await self._uow.quizzes_repo.create_quiz_localization(
                        {
                            "quiz_id": quiz.id,
                            "language": loc.get("language"),
                            "title": loc.get("title"),
                            "description": loc.get("description"),
                        }
                    )
                await uow.commit()
                return quiz
            except Exception as e:
                await uow.rollback()
                raise e

    async def quizzes_list(
        self, offset: int, limit: int, x_language_code: LanguageCode
    ):
        async with self._uow as uow:
            quizzes = await uow.quizzes_repo.get_all(
                x_language_code.value, offset, limit
            )
            print(quizzes)
            return {"quizzes": [
                {
                    'quiz_id':q.quiz_id,
                    'language':q.language,
                    'title':q.title,
                    'description':q.description
                }
                for q in quizzes
            ], "count": len(quizzes)}
