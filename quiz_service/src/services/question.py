from uuid import UUID

from src.core.exceptions.base import BadRequestException
from src.core.uow import UnitOfWork
from src.schemas.requests.question import QuestionCreateRequest


class QuestionService:

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def add_questions(
        self, question_data: QuestionCreateRequest, quiz_id: UUID
    ) -> dict:
        async with self._uow as uow:
            try:
                if await uow.quizzes_repo.get_by_id(quiz_id) is None:
                    raise BadRequestException("Quiz not found")

                question = await uow.question_repo.create_question(
                    {
                        "quiz_id": quiz_id,
                        "question_type": question_data.question_type,
                    }
                )
                for q_loc in question_data.localizations:
                    await uow.question_repo.create_question_localization(
                        {
                            "question_id": question.id,
                            "language": q_loc.language.value,
                            "question_text": q_loc.question_text,
                            "content": q_loc.content.model_dump(),
                        }
                    )
                await uow.commit()
                return question
            except Exception as e:
                await uow.rollback()
                raise e

    async def get_questions(self, quiz_id: UUID, x_language_code):
        async with self._uow as uow:
            try:
                questions_list = await uow.question_repo.get_list_by_quiz_id(
                    quiz_id, x_language_code
                )
                res = [
                    {
                        "question_id": q.question.id,
                        "question_type": q.question.question_type,
                        "local_question_id": q.id,
                        "question_text": q.question_text,
                        "content": q.content.get("public_data"),
                    }
                    for q in questions_list
                ]
                return res
            except Exception as e:
                raise e
