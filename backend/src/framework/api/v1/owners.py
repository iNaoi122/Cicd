from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.business.dto.owner_dto import OwnerCreateDTO
from src.business.operations.owner_operations import (
    create_owner,
    get_owner_by_id,
    list_owners,
)
from src.data.uow import UnitOfWork
from src.framework.dependencies import get_db
from src.framework.schemas import OwnerCreate, OwnerResponse

router = APIRouter(prefix="/owners", tags=["owners"])


@router.post("/", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
async def create_owner_endpoint(
    owner_data: OwnerCreate, session: AsyncSession = Depends(get_db)
):
    """Создать нового владельца"""
    try:
        uow = UnitOfWork(session)
        dto = OwnerCreateDTO(
            name=owner_data.name,
            address=owner_data.address,
            phone=owner_data.phone,
        )
        owner = await create_owner(uow, dto)
        return owner
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{owner_id}", response_model=OwnerResponse)
async def get_owner_endpoint(owner_id: int, session: AsyncSession = Depends(get_db)):
    """Получить владельца по ID"""
    uow = UnitOfWork(session)
    owner = await get_owner_by_id(uow, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Владелец не найден")
    return owner


@router.get("/", response_model=List[OwnerResponse])
async def list_owners_endpoint(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db)
):
    """Получить список владельцев"""
    uow = UnitOfWork(session)
    owners = await list_owners(uow, skip=skip, limit=limit)
    return owners
