from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import HTTPException

from src.core.enums import EventType
from src.core.exceptions.base import BadRequestException, NotFoundException
from src.core.uow import UnitOfWork
from src.schemas.requests.question import QuestionCreateRequest
from src.services.rabbit_mq import RMQEventPublisher


class UserQuizSessionService:

    def __init__(self, uow: UnitOfWork, publisher: RMQEventPublisher):
        self._uow = uow
        self.publisher = publisher

    async def start_quiz_session(self, quiz_id: UUID, user_id: UUID):
        async with self._uow as uow:
            try:
                new_session = await uow.user_quiz_session_repo.create(
                    {
                        "user_id": user_id,
                        "quiz_id": quiz_id,
                    }
                )
                await uow.commit()
                return new_session
            except Exception as e:
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
                # if user_quiz_session.is_completed:
                #     raise BadRequestException("Session already completed")

                new_correct_question_count = await self._calculate_correct_questions(
                    uow, session_id, user_id
                )
                user_quiz_session.is_completed = True
                user_quiz_session.ended_at = datetime.utcnow()

                await uow.commit()
                response = {
                    "event_type": EventType.QUIZ_COMPLETED.value,
                    "session_id": str(session_id),
                    "user_id": str(user_id),
                    "streak": 2,
                    "new_correct_answers": new_correct_question_count,
                    "completion_time": str(user_quiz_session.ended_at),
                }
                await self.publisher.publish_event(event_payload=response)
                return response
            except Exception as e:
                await uow.rollback()
                raise e

    async def get_session_info(
        self,
        session_id: UUID,
    ):
        async with self._uow as uow:
            try:
                session = await uow.user_quiz_session_repo.get_by_id(session_id)
                if session is None:
                    raise NotFoundException("Session not found")
                return session
            except Exception as e:
                raise e

    async def _calculate_correct_questions(
        self, uow: UnitOfWork, session_id: UUID, user_id: UUID
    ):
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
