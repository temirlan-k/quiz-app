from uuid import UUID
from fastapi import APIRouter, Depends, Header
from src.services.balance_service import BalanceService
from dependency_injector.wiring import inject,Provide
from src.core.containers import Container

balance_router = APIRouter(tags=['/balances'])

@balance_router.get("/my-balance")
@inject
async def current_user_balance(
    x_user_id: UUID = Header(...),
    balance_service:BalanceService = Depends(Provide[Container.balance_service])
):
    return await balance_service.award_balance(x_user_id,100)