from dependency_injector.wiring import Provide, inject

from fastapi import APIRouter, Depends, Header

from src.core.containers import Container
from src.core.enums import LanguageCode
from src.schemas.requests.quiz import QuizCreateRequest
from src.services.quiz import QuizService

quiz_router = APIRouter(prefix="/quizzes", tags=["QUIZZES"])


@quiz_router.post(
    "/",
    summary="Create a new Quiz with Questions",
    description="Creates a new quiz along with its questions and localizations based on the provided data.",
)
@inject
async def create_quiz_with_questions(
    quiz_data: QuizCreateRequest,
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),
):
    """
    Create a new quiz with associated questions.
    - **quiz_data**: Data for creating a quiz, including localizations and questions.
    """
    return await quiz_service.create_quiz(quiz_data.model_dump())


@quiz_router.get(
    "/",
    summary="Get a list of Quizzes",
    description="Retrieves a list of quizzes localized based on the provided language code, with pagination support.",
)
@inject
async def quizzes_list(
    offset: int = 0,
    limit: int = 10,
    x_language_code: LanguageCode = Header(...),
    quiz_service: QuizService = Depends(Provide[Container.quiz_service]),
):
    """
    Retrieve a paginated list of quizzes.
    - **offset**: Starting position of the list.
    - **limit**: Maximum number of quizzes to return.
    - **x_language_code**: Language code provided in the header to localize quiz information.
    """
    return await quiz_service.quizzes_list(offset, limit, x_language_code)
