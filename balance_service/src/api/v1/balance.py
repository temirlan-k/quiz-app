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
    return await balance_service.award_balance(x_user_id, 100)
