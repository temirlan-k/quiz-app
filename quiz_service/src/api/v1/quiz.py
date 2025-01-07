from fastapi import APIRouter, Depends, Header
from dependency_injector.wiring import inject, Provide
from src.schemas.requests.quiz import QuizCreateRequest
from src.services.quiz import QuizService
from src.core.containers import Container
from src.core.enums import LanguageCode

quiz_router = APIRouter(prefix='/quizzes',tags=['QUIZZES'])


@quiz_router.post("/")
@inject
async def create_quiz_with_questions(
    quiz_data: QuizCreateRequest,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service])
):
    return await quiz_service.create_quiz(quiz_data.model_dump())

@quiz_router.get('/')
@inject
async def quizzes_list(
    offset: int = 0,
    limit: int = 10,
    x_language_code: LanguageCode = Header(...),
    quiz_service: QuizService = Depends(Provide[Container.quiz_service])
):
    return await quiz_service.quizzes_list(offset, limit,x_language_code)