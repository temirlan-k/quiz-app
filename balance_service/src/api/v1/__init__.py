from fastapi import APIRouter
from src.api.v1.balance import balance_router

router = APIRouter(prefix='/api/v1')

router.include_router(balance_router)
