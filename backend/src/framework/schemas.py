import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Схемы для Race
class RaceCreate(BaseModel):
    """Схема для создания состязания"""

    model_config = ConfigDict(populate_by_name=True)

    race_date: datetime.date = Field(
        ..., description="Дата проведения состязания", alias="date"
    )
    race_time: datetime.time = Field(..., description="Время проведения", alias="time")
    hippodrome: str = Field(..., min_length=1, max_length=200)
    name: Optional[str] = Field(None, max_length=200)


class RaceResponse(BaseModel):
    """Схема ответа для состязания"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime.date = Field(..., description="Дата проведения состязания")
    time: datetime.time = Field(..., description="Время проведения")
    hippodrome: str
    name: Optional[str]


class ParticipantResultResponse(BaseModel):
    """Результат участника"""

    jockey_name: str
    horse_name: str
    place: int
    time_result: Optional[datetime.time] = None


class RaceWithParticipantsResponse(BaseModel):
    """Состязание с участниками и результатами"""

    race: RaceResponse
    participants: list[ParticipantResultResponse]


# Схемы для Jockey
class JockeyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: str = Field(..., min_length=1, max_length=500)
    age: int = Field(..., gt=0, lt=150)
    rating: int = Field(..., ge=0)


class JockeyCreate(JockeyBase):
    """Схема для создания жокея"""

    pass


class JockeyResponse(JockeyBase):
    """Схема ответа для жокея"""

    id: int

    model_config = ConfigDict(from_attributes=True)


# Схемы для Horse
class HorseBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., pattern="^(жеребец|кобыла|мерин)$")
    age: int = Field(..., gt=0, lt=50)
    owner_id: int = Field(..., gt=0)


class HorseCreate(HorseBase):
    """Схема для создания лошади"""

    pass


class HorseResponse(HorseBase):
    """Схема ответа для лошади"""

    id: int

    model_config = ConfigDict(from_attributes=True)


# Схемы для Owner
class OwnerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: str = Field(..., min_length=1, max_length=500)
    phone: str = Field(..., min_length=1, max_length=20)


class OwnerCreate(OwnerBase):
    """Схема для создания владельца"""

    pass


class OwnerResponse(OwnerBase):
    """Схема ответа для владельца"""

    id: int

    model_config = ConfigDict(from_attributes=True)


# Схемы для Participant
class ParticipantCreate(BaseModel):
    """Схема для добавления результата участника"""

    race_id: int = Field(..., gt=0)
    jockey_id: int = Field(..., gt=0)
    horse_id: int = Field(..., gt=0)
    place: int = Field(..., gt=0)
    time_result: Optional[datetime.time] = None


class ParticipantResponse(BaseModel):
    """Схема ответа для участника"""

    id: int
    race_id: int
    jockey_id: int
    horse_id: int
    place: int
    time_result: Optional[datetime.time]

    model_config = ConfigDict(from_attributes=True)
