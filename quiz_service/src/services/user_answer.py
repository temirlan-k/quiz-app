
from datetime import datetime
from typing import List
from uuid import UUID
from src.core.uow import UnitOfWork
from src.schemas.requests.question import QuestionCreateRequest
from src.core.exceptions.base import BadRequestException,NotFoundException
from src.models.question import Question,QuestionLocalization
from src.core.enums import QuestionType
from src.services.answer.answer_checkers import AnswerCheckerFactory
from src.services.answer.feeback_provider import FeedbackProviderFactory


class AnswerService:

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def answer_question(self,question_id: UUID, user_id: UUID, answer_request:dict,language_code: str):
        async with self._uow as uow:
            try:
                question_l = await uow.question_repo.get_localized_question(question_id,language_code)
                if question_l is None:
                    raise NotFoundException("Question not found")
                
                checker = AnswerCheckerFactory.get_checker(question_l.question.question_type)
                is_correct = checker.check_answer(question_l,answer_request)
                attempt = await uow.user_attempt_repo.create({
                    "user_id":user_id,
                    "quiz_id":question_l.question.quiz_id,
                    "question_id":question_id,
                    "session_id":answer_request.get("session_id"),
                    "answer_content":answer_request.get("answer_content"),
                    "is_correct":is_correct
                })
                if not is_correct:
                    feedback = FeedbackProviderFactory.get_provider(question_l.question.question_type)

                await uow.commit()
                return {
                    "question_id":attempt.question_id,
                    "is_correct":attempt.is_correct,
                    "feedback": feedback
                }
            except Exception as e:
                await uow.rollback()
                raise e
            
