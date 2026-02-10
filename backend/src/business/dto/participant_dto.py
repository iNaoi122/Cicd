from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ParticipantCreateDTO(BaseModel):
    """DTO для создания участника"""

    race_id: int = Field(..., gt=0)
    jockey_id: int = Field(..., gt=0)
    horse_id: int = Field(..., gt=0)
    place: int = Field(..., gt=0)
    time_result: Optional[time] = None


class ParticipantDTO(BaseModel):
    """DTO участника"""

    id: int
    race_id: int
    jockey_id: int
    horse_id: int
    place: int
    time_result: Optional[time]

    model_config = ConfigDict(from_attributes=True)
