from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header
from pydantic import UUID4

from src.core.containers import Container
from src.core.enums import LanguageCode
from src.schemas.requests.question import (
    QuestionCreateRequest,
    AnswerQuestionStandard,
    AnswerQuestionMatching,
)
from src.services.question import QuestionService
from src.services.user_answer import AnswerService

question_router = APIRouter(prefix="/questions", tags=["QUESTIONS"])


@question_router.post(
    "/add/{quiz_id}",
    summary="Add Questions to a Quiz",
    description="Create and add new questions to the specified quiz by quiz_id.",
)
@inject
async def create_quiz_question(
    quiz_id: UUID4,
    question_data: QuestionCreateRequest,
    question_service: QuestionService = Depends(Provide[Container.question_service]),
):
    """
    Create and add new questions to a quiz.
    - **quiz_id**: UUID of the quiz
    - **question_data**: Data for creating questions
    """
    return await question_service.add_questions(question_data, quiz_id)


@question_router.get(
    "/{quiz_id}",
    summary="Get Questions for a Quiz",
    description="Retrieve a list of questions for the specified quiz, localized by language code provided in the header.",
)
@inject
async def get_questions(
    quiz_id: UUID4,
    x_language_code: LanguageCode = Header(...),
    question_service: QuestionService = Depends(Provide[Container.question_service]),
):
    """
    Retrieve a list of questions for the given quiz ID, using the language specified in the header.
    - **quiz_id**: UUID of the quiz
    - **x_language_code**: Language code provided in the request header
    """
    return await question_service.get_questions(quiz_id, x_language_code)


@question_router.post(
    "/{question_id}/answer",
    summary="Answer a Standard Question",
    description="Submit an answer for a standard question (e.g., Single Choice, Multiple Choice, Fill in the Blank).",
)
@inject
async def answer_to_question(
    question_id: UUID,
    answer_request: AnswerQuestionStandard,
    x_language_code: LanguageCode = Header(...),
    x_user_id: UUID4 = Header(...),
    answer_service: AnswerService = Depends(Provide[Container.answer_service]),
):
    """
    Submit an answer for a standard question.
    - **question_id**: UUID of the question
    - **answer_request**: The request body containing the answer data
    - **x_language_code**: Language code provided in the header
    - **x_user_id**: User ID provided in the header
    """
    return await answer_service.answer_question(
        question_id, x_user_id, answer_request.model_dump(), x_language_code
    )


@question_router.post(
    "/{question_id}/answer-matching",
    summary="Answer a Matching Question",
    description="Submit an answer for a matching question. All pairs must be provided.",
)
@inject
async def answer_to_question_matching(
    question_id: UUID,
    answer_request: AnswerQuestionMatching,
    x_language_code: LanguageCode = Header(...),
    x_user_id: UUID4 = Header(...),
    answer_service: AnswerService = Depends(Provide[Container.answer_service]),
):
    """
    Submit an answer for a matching question.
    - **question_id**: UUID of the question
    - **answer_request**: The request body containing the matching answer data
    - **x_language_code**: Language code provided in the header
    - **x_user_id**: User ID provided in the header
    """
    return await answer_service.answer_question(
        question_id, x_user_id, answer_request.model_dump(), x_language_code
    )
