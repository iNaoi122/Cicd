from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.business.dto.race_dto import RaceCreateDTO
from src.business.operations.race_operations import (
    create_race,
    get_race_with_participants,
    list_races,
)
from src.data.uow import UnitOfWork
from src.framework.dependencies import get_db
from src.framework.schemas import RaceCreate, RaceResponse, RaceWithParticipantsResponse

router = APIRouter(prefix="/races", tags=["races"])


@router.get("/", response_model=List[RaceResponse])
async def list_races_endpoint(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db)
):
    """Получить список всех состязаний"""
    uow = UnitOfWork(session)
    races = await list_races(uow, skip=skip, limit=limit)
    return races


@router.post("/", response_model=RaceResponse, status_code=status.HTTP_201_CREATED)
async def create_race_endpoint(
    race_data: RaceCreate, session: AsyncSession = Depends(get_db)
):
    """Создать новое состязание (Функция 2 из ТЗ)"""
    try:
        uow = UnitOfWork(session)
        dto = RaceCreateDTO(
            date=race_data.race_date,
            time=race_data.race_time,
            hippodrome=race_data.hippodrome,
            name=race_data.name,
        )
        race = await create_race(uow, dto)
        return race
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{race_id}", response_model=RaceWithParticipantsResponse)
async def get_race_endpoint(race_id: int, session: AsyncSession = Depends(get_db)):
    """
    Получить состязание с участниками и результатами
    (Функция 1 из ТЗ)
    """
    uow = UnitOfWork(session)
    race_data = await get_race_with_participants(uow, race_id)
    if not race_data:
        raise HTTPException(status_code=404, detail="Состязание не найдено")
    return race_data
