from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import HTTPException
from src.core.uow import UnitOfWork
from src.schemas.requests.question import QuestionCreateRequest
from src.core.exceptions.base import BadRequestException,NotFoundException



class UserQuizSessionService:
    
    def __init__(self,uow:UnitOfWork):
        self._uow = uow

    async def start_quiz_session(self,quiz_id: UUID, user_id: UUID):
        async with self._uow as uow:
            try:
                new_session = await uow.user_quiz_session_repo.create({
                    "user_id":user_id,
                    "quiz_id":quiz_id,
                })
                await uow.commit()
                return new_session
            except Exception as e:
                await uow.rollback()
                raise e


    async def complete_quiz_session(self, user_id: UUID, session_id: UUID) -> dict:
        async with self._uow as uow:
            try:
                user_quiz_session = await uow.user_quiz_session_repo.get_user_session(user_id, session_id)
                if user_quiz_session is None or user_quiz_session.user_id != user_id:
                    raise NotFoundException("Session not found")
                if user_quiz_session.is_completed:
                    raise BadRequestException("Session already completed")
                

                correct_attempts = await uow.user_attempt_repo.get_correct_attempts_by_question_in_session(
                    session_id=session_id,
                    user_id=user_id
                )
                balance_to_award = 0
                counted_questions = set()
                for attempt in correct_attempts:
                    if attempt.question_id in counted_questions:
                        continue

                    # Check if this question was answered correctly in any previous session
                    was_answered_correctly_before = await uow.user_attempt_repo.check_correct_past(
                        user_id=user_id,
                        question_id=attempt.question_id,
                        current_session_id=session_id
                    )

                    if not was_answered_correctly_before:
                        balance_to_award += 1
                        counted_questions.add(attempt.question_id)


                user_quiz_session.is_completed = True
                user_quiz_session.ended_at = datetime.utcnow()

                await uow.commit()
                return {
                    "session_id": session_id,
                    "counted_questions": list(counted_questions),
                    "balance_awarded": balance_to_award,
                    "completion_time": user_quiz_session.ended_at
                }
            except Exception as e:
                await uow.rollback()
                raise e


    async def get_session_info(self, session_id:UUID,):
        async with self._uow as uow:
            try:
                session =await uow.user_quiz_session_repo.get_by_id(session_id)
                if session is None:
                    raise NotFoundException('Session not found')
                return session
            except Exception as e:
                raise e