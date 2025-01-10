from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header
from pydantic import UUID4

from src.core.containers import Container
from src.core.enums import LanguageCode
from src.schemas.requests.quiz import QuizCreateRequest
from src.services.quiz import QuizService
from src.services.user_quiz_session import UserQuizSessionService

quiz_session_router = APIRouter(prefix="/quiz_sessions", tags=["QUIZ SESSIONS"])


@quiz_session_router.post("/{quiz_id}/start-session")
@inject
async def start_session(
    quiz_id: UUID4,
    x_user_id: UUID4 = Header(...),
    quiz_session_service: UserQuizSessionService = Depends(
        Provide[Container.quiz_session_service]
    ),
):
    return await quiz_session_service.start_quiz_session(quiz_id, x_user_id)


@quiz_session_router.get("/{session_id}")
@inject
async def get_session_info(
    session_id: UUID4,
    quiz_session_service: UserQuizSessionService = Depends(
        Provide[Container.quiz_session_service]
    ),
):
    return await quiz_session_service.get_session_info(session_id)


@quiz_session_router.post("/{session_id}/finish-session")
@inject
async def finish_session(
    session_id: UUID4,
    x_user_id: UUID4 = Header(...),
    quiz_session_service: UserQuizSessionService = Depends(
        Provide[Container.quiz_session_service]
    ),
):
    return await quiz_session_service.complete_quiz_session(x_user_id, session_id)
