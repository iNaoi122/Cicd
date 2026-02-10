from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.business.dto.jockey_dto import JockeyCreateDTO
from src.business.operations.jockey_operations import (
    create_jockey,
    get_jockey_by_id,
    list_jockeys,
)
from src.business.operations.race_operations import get_jockey_races
from src.data.uow import UnitOfWork
from src.framework.dependencies import get_db
from src.framework.schemas import JockeyCreate, JockeyResponse, RaceResponse

router = APIRouter(prefix="/jockeys", tags=["jockeys"])


@router.get("/", response_model=List[JockeyResponse])
async def list_jockeys_endpoint(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db)
):
    """Получить список жокеев"""
    uow = UnitOfWork(session)
    jockeys = await list_jockeys(uow, skip=skip, limit=limit)
    return jockeys


@router.post("/", response_model=JockeyResponse, status_code=status.HTTP_201_CREATED)
async def create_jockey_endpoint(
    jockey_data: JockeyCreate, session: AsyncSession = Depends(get_db)
):
    """Создать нового жокея (Функция 3 из ТЗ)"""
    try:
        uow = UnitOfWork(session)
        dto = JockeyCreateDTO(
            name=jockey_data.name,
            address=jockey_data.address,
            age=jockey_data.age,
            rating=jockey_data.rating,
        )
        jockey = await create_jockey(uow, dto)
        return jockey
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{jockey_id}/races", response_model=List[RaceResponse])
async def get_jockey_races_endpoint(
    jockey_id: int, session: AsyncSession = Depends(get_db)
):
    """
    Получить список состязаний жокея
    (Функция 6 из ТЗ)
    """
    try:
        uow = UnitOfWork(session)
        races = await get_jockey_races(uow, jockey_id)
        return races
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{jockey_id}", response_model=JockeyResponse)
async def get_jockey_endpoint(jockey_id: int, session: AsyncSession = Depends(get_db)):
    """Получить жокея по ID"""
    uow = UnitOfWork(session)
    jockey = await get_jockey_by_id(uow, jockey_id)
    if not jockey:
        raise HTTPException(status_code=404, detail="Жокей не найден")
    return jockey
