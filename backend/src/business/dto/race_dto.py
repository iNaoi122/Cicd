import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RaceCreateDTO(BaseModel):
    """DTO для создания состязания"""

    date: datetime.date
    time: datetime.time
    hippodrome: str
    name: Optional[str] = None


class RaceDTO(BaseModel):
    """DTO состязания"""

    id: int
    date: datetime.date
    time: datetime.time
    hippodrome: str
    name: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ParticipantResultDTO(BaseModel):
    """DTO результата участника"""

    jockey_name: str
    horse_name: str
    place: int
    time_result: Optional[datetime.time] = None


class RaceWithParticipantsDTO(BaseModel):
    """DTO состязания с участниками"""

    race: RaceDTO
    participants: list[ParticipantResultDTO]
