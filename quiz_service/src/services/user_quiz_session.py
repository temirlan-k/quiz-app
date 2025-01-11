import logging
from datetime import datetime
from uuid import UUID

from src.core.enums import EventType
from src.core.exceptions import BadRequestException, NotFoundException
from src.core.uow import UnitOfWork
from src.services.rabbit_mq import RMQEventPublisher
from src.models.quiz_session import UserQuizSession

logger = logging.getLogger(__name__)


class UserQuizSessionService:

    def __init__(self, uow: UnitOfWork, publisher: RMQEventPublisher):
        self._uow = uow
        self.publisher = publisher

    async def start_quiz_session(self, quiz_id: UUID, user_id: UUID) -> UserQuizSession:
        async with self._uow as uow:
            try:
                total_questions = await uow.question_repo.count_questions(quiz_id)
                new_session = await uow.user_quiz_session_repo.create(
                    {
                        "user_id": user_id,
                        "quiz_id": quiz_id,
                        "total_questions": total_questions,
                    }
                )
                await uow.commit()
                return new_session
            except Exception as e:
                logger.error(f"Error starting quiz session: {e}", exc_info=True)
                await uow.rollback()
                raise e

    async def complete_quiz_session(self, user_id: UUID, session_id: UUID) -> dict:
        async with self._uow as uow:
            try:
                user_quiz_session = await uow.user_quiz_session_repo.get_user_session(
                    user_id, session_id
                )
                if user_quiz_session is None or user_quiz_session.user_id != user_id:
                    raise NotFoundException("Session not found")
                if user_quiz_session.is_completed:
                    raise BadRequestException("Session already completed")

                new_correct_question_count = await self._calculate_correct_questions(
                    uow, session_id, user_id
                )

                user_quiz_session.is_completed = True
                user_quiz_session.ended_at = datetime.now()
                quiz_id = user_quiz_session.quiz_id
                user_score = user_quiz_session.score
                current_streak = user_quiz_session.current_streak

                percentile = await uow.user_quiz_session_repo.get_percentile_rank(
                    quiz_id, user_score
                )
                response = {
                    "event_type": EventType.QUIZ_COMPLETED.value,
                    "session_id": str(session_id),
                    "user_id": str(user_id),
                    "current_streak": current_streak,
                    "percentile": percentile,
                    "score": user_quiz_session.score,
                    "new_correct_answers": new_correct_question_count,
                }
                await self.publisher.publish_event(event_payload=response)
                await uow.commit()
                return response
            except Exception as e:
                logger.error(f"Error completing quiz session: {e}", exc_info=True)
                await uow.rollback()
                raise e

    async def get_session_info(
        self,
        session_id: UUID,
    ) -> UserQuizSession:
        async with self._uow as uow:
            try:
                session = await uow.user_quiz_session_repo.get_by_id(session_id)
                if session is None:
                    raise NotFoundException("Session not found")
                return session
            except Exception as e:
                logger.error(f"Error getting session info: {e}", exc_info=True)
                raise e

    async def _calculate_correct_questions(
        self, uow: UnitOfWork, session_id: UUID, user_id: UUID
    ) -> int:
        correct_attempts = await uow.user_attempt_repo.get_correct_attempts_in_session(
            session_id=session_id, user_id=user_id
        )
        new_correct_question_count = 0
        counted_questions = set()
        for q in correct_attempts:
            if q.question_id in counted_questions:
                continue
            was_answered_correctly_before = (
                await uow.user_attempt_repo.check_correct_past(
                    user_id, q.question_id, session_id
                )
            )
            if not was_answered_correctly_before:
                new_correct_question_count += 1
            counted_questions.add(q.question_id)
        return new_correct_question_count
