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


    async def complete_quiz_session(self,user_id: UUID, session_id: UUID)->dict:
        async with self._uow as uow:
            try:
                quiz_session = await uow.user_quiz_session_repo.get_user_sessions(session_id)
                if quiz_session is None or quiz_session.user_id != user_id:
                    raise NotFoundException("Session not found")
                quiz_session.is_completed = True
                quiz_session.ended_at = datetime.utcnow()
                await uow.flush()
                correct_questions = await uow.user_attempt_repo.get_correct_questions(session_id,user_id)
                new_correct_question_count = 0
                for q in correct_questions:
                    was_answered_correctly_before = await uow.user_attempt_repo.check_correct_past(user_id,q.question_id,session_id)
                    if not was_answered_correctly_before:
                        new_correct_question_count += 1
                return new_correct_question_count
            except Exception as e:
                await uow.rollback()
                raise e