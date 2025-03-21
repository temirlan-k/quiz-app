import logging
from uuid import UUID

from src.core.exceptions import BadRequestException, NotFoundException
from src.core.uow import UnitOfWork
from src.models.question import QuestionLocalization
from src.services.answer.answer_checkers import AnswerCheckerFactory
from src.services.answer.feeback_provider import FeedbackProviderFactory
from src.models.quiz_session import UserQuizSession

logger = logging.getLogger(__name__)


class AnswerService:

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def answer_question(
        self, question_id: UUID, user_id: UUID, answer_request: dict, language_code: str
    ) -> dict:
        async with self._uow as uow:
            try:
                session_id = answer_request.get("session_id")
                answer_content = answer_request.get("answer_content")

                user_quiz_session = await uow.user_quiz_session_repo.get_by_id(
                    session_id
                )
                if not user_quiz_session:
                    raise NotFoundException("Session not found")

                question_l = await uow.question_repo.get_localized_question(
                    question_id, language_code
                )
                if question_l is None:
                    raise NotFoundException("Question not found")

                await self._check_repeat_attempts(
                    uow, question_l, user_id, answer_request
                )

                checker = AnswerCheckerFactory.get_checker(
                    question_l.question.question_type
                )
                is_correct = checker.check_answer(question_l, answer_content)

                await self._update_streak_and_score(user_quiz_session, is_correct)

                attempt = await uow.user_attempt_repo.create(
                    {
                        "user_id": user_id,
                        "quiz_id": question_l.question.quiz_id,
                        "question_id": question_id,
                        "session_id": session_id,
                        "answer_content": answer_content,
                        "is_correct": is_correct,
                    }
                )

                attempt_feedback = "Correct!"
                if not is_correct:
                    provider = FeedbackProviderFactory.get_provider(
                        question_l.question.question_type
                    )
                    attempt_feedback = provider.generate_feedback(question_l)

                await uow.commit()
                return {
                    "question_id": attempt.question_id,
                    "is_correct": attempt.is_correct,
                    "feedback": attempt_feedback,
                    "current_streak": user_quiz_session.current_streak,
                }
            except Exception as e:
                logger.error(f"Error in answer_question: {e}", exc_info=True)
                await uow.rollback()
                raise e

    async def _check_repeat_attempts(
        self,
        uow: UnitOfWork,
        question_l: QuestionLocalization,
        user_id,
        answer_request: dict,
    ) -> None:
        existing_attempt = await uow.user_attempt_repo.get_by_user_question_session(
            user_id,
            question_l.question.id,
            answer_request.get("session_id"),
        )
        if existing_attempt:
            raise BadRequestException("You can't rewrite your choice")

    async def _update_streak_and_score(
        self, user_quiz_session: UserQuizSession, is_correct: bool
    ) -> None:
        if is_correct:
            user_quiz_session.current_streak += 1
            user_quiz_session.score += 1
            if user_quiz_session.current_streak > user_quiz_session.max_streak:
                user_quiz_session.max_streak = user_quiz_session.current_streak
        else:
            user_quiz_session.current_streak = 0
