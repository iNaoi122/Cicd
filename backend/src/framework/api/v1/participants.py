from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.business.dto.participant_dto import ParticipantCreateDTO
from src.business.operations.participant_operations import add_participant_with_result
from src.data.uow import UnitOfWork
from src.framework.dependencies import get_db
from src.framework.schemas import ParticipantCreate, ParticipantResponse

router = APIRouter(prefix="/participants", tags=["participants"])


@router.post(
    "/", response_model=ParticipantResponse, status_code=status.HTTP_201_CREATED
)
async def add_participant_endpoint(
    participant_data: ParticipantCreate, session: AsyncSession = Depends(get_db)
):
    """
    Добавить результат участника в состязании
    (Функция 5 из ТЗ)
    """
    try:
        uow = UnitOfWork(session)
        dto = ParticipantCreateDTO(
            race_id=participant_data.race_id,
            jockey_id=participant_data.jockey_id,
            horse_id=participant_data.horse_id,
            place=participant_data.place,
            time_result=participant_data.time_result,
        )
        participant = await add_participant_with_result(uow, dto)
        return participant
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
