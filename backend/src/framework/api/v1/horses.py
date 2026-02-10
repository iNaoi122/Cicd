from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.business.dto.horse_dto import HorseCreateDTO
from src.business.operations.horse_operations import (
    create_horse,
    get_horse_by_id,
    list_horses,
)
from src.business.operations.race_operations import get_horse_races
from src.data.uow import UnitOfWork
from src.framework.dependencies import get_db
from src.framework.schemas import HorseCreate, HorseResponse, RaceResponse

router = APIRouter(prefix="/horses", tags=["horses"])


@router.get("/", response_model=List[HorseResponse])
async def list_horses_endpoint(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db)
):
    """Получить список лошадей"""
    uow = UnitOfWork(session)
    horses = await list_horses(uow, skip=skip, limit=limit)
    return horses


@router.post("/", response_model=HorseResponse, status_code=status.HTTP_201_CREATED)
async def create_horse_endpoint(
    horse_data: HorseCreate, session: AsyncSession = Depends(get_db)
):
    """Создать новую лошадь (Функция 4 из ТЗ)"""
    try:
        uow = UnitOfWork(session)
        dto = HorseCreateDTO(
            nickname=horse_data.nickname,
            gender=horse_data.gender,
            age=horse_data.age,
            owner_id=horse_data.owner_id,
        )
        horse = await create_horse(uow, dto)
        return horse
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{horse_id}/races", response_model=List[RaceResponse])
async def get_horse_races_endpoint(
    horse_id: int, session: AsyncSession = Depends(get_db)
):
    """
    Получить список состязаний лошади
    (Функция 7 из ТЗ)
    """
    try:
        uow = UnitOfWork(session)
        races = await get_horse_races(uow, horse_id)
        return races
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{horse_id}", response_model=HorseResponse)
async def get_horse_endpoint(horse_id: int, session: AsyncSession = Depends(get_db)):
    """Получить лошадь по ID"""
    uow = UnitOfWork(session)
    horse = await get_horse_by_id(uow, horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Лошадь не найдена")
    return horse
