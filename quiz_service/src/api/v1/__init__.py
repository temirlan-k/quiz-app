from fastapi import APIRouter
from src.api.v1.quiz import quiz_router
from src.api.v1.question import question_router

router = APIRouter(prefix='/api/v1')

router.include_router(quiz_router)
router.include_router(question_router)