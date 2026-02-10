from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.data.models import GenderEnum


class HorseCreateDTO(BaseModel):
    """DTO для создания лошади"""

    nickname: str = Field(..., min_length=1)
    gender: str = Field(..., pattern="^(жеребец|кобыла|мерин)$")
    age: int = Field(..., gt=0)
    owner_id: int = Field(..., gt=0)


class HorseDTO(BaseModel):
    """DTO лошади"""

    id: int
    nickname: str
    gender: str
    age: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("gender", mode="before")
    @classmethod
    def convert_gender_enum(cls, v):
        if isinstance(v, GenderEnum):
            return v.value
        return v
