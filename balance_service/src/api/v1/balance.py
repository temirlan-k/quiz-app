from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header

from src.core.containers import Container
from src.services.balance_service import BalanceService

balance_router = APIRouter(tags=["/balances"])


@balance_router.get("/my-balance")
@inject
async def current_user_balance(
    x_user_id: UUID = Header(...),
    balance_service: BalanceService = Depends(Provide[Container.balance_service]),
):
    return await balance_service.my_balance(x_user_id)


@balance_router.post('/update',response_model=None)
@inject
async def update(
    x_user_id: UUID = Header(...),
    balance_service: BalanceService = Depends(Provide[Container.balance_service]),
):
    return await balance_service.process_quiz_completion(x_user_id,5,2)