from dependency_injector.wiring import Provide, inject

from fastapi import APIRouter, Depends, Header
from pydantic import UUID4

from src.core.containers import Container
from src.services.user_quiz_session import UserQuizSessionService

quiz_session_router = APIRouter(prefix="/quiz_sessions", tags=["QUIZ SESSIONS"])


@quiz_session_router.post(
    "/start-session/{quiz_id}",
    summary="Start a new quiz session",
    description="Begins a new session for a given quiz and user.",
)
@inject
async def start_session(
    quiz_id: UUID4,
    x_user_id: UUID4 = Header(...),
    quiz_session_service: UserQuizSessionService = Depends(
        Provide[Container.quiz_session_service]
    ),
):
    """
    Start a new quiz session for the specified quiz.

    - **quiz_id**: UUID of the quiz to start.
    - **x_user_id**: UUID of the user starting the session (provided in header).
    """
    return await quiz_session_service.start_quiz_session(quiz_id, x_user_id)


@quiz_session_router.get(
    "/{session_id}",
    summary="Get session info",
    description="Retrieve information about a specific quiz session.",
)
@inject
async def get_session_info(
    session_id: UUID4,
    quiz_session_service: UserQuizSessionService = Depends(
        Provide[Container.quiz_session_service]
    ),
):
    """
    Get information for a given quiz session.

    - **session_id**: UUID of the quiz session to retrieve.
    """
    return await quiz_session_service.get_session_info(session_id)


@quiz_session_router.post(
    "/finish-session/{session_id}",
    summary="Finish a quiz session",
    description="Marks the specified quiz session as completed and calculates results.",
)
@inject
async def finish_session(
    session_id: UUID4,
    x_user_id: UUID4 = Header(...),
    quiz_session_service: UserQuizSessionService = Depends(
        Provide[Container.quiz_session_service]
    ),
):
    """
    Finish the quiz session.

    - **session_id**: UUID of the session to finish.
    - **x_user_id**: UUID of the user finishing the session (provided in header).
    """
    return await quiz_session_service.complete_quiz_session(x_user_id, session_id)
