from typing import List
from fastapi import APIRouter, Depends, Header
from pydantic import UUID4
from dependency_injector.wiring import inject, Provide
from src.services.user_answer import AnswerService
from src.core.enums import LanguageCode
from src.services.question import QuestionService
from src.schemas.requests.quiz import QuizCreateRequest
from src.services.quiz import QuizService
from src.core.containers import Container
from src.schemas.requests.question import QuestionCreateRequest


question_router = APIRouter(prefix='/questions',tags=['QUESTIONS'])


@question_router.post("/{quiz_id}/add")
@inject
async def create_quiz_question(
    quiz_id: UUID4,
    question_data: QuestionCreateRequest,
    question_service: QuestionService = Depends(Provide[Container.question_service])
):
    return await question_service.add_questions(question_data,quiz_id)


@question_router.get("/{quiz_id}")
@inject
async def get_questions(
    quiz_id: UUID4,
    x_language_code: LanguageCode = Header(...),
    question_service: QuestionService = Depends(Provide[Container.question_service])
):
    return await question_service.get_questions(quiz_id,x_language_code)


@question_router.post("/{question_id}/answer")
@inject
async def answer_to_question(
    question_id: UUID4,answer_request: dict,
    x_language_code: LanguageCode = Header(...), x_user_id: UUID4 = Header(...),
    answer_service: AnswerService = Depends(Provide[Container.answer_service])
):
    return await answer_service.answer_question(question_id,x_user_id,answer_request,x_language_code)