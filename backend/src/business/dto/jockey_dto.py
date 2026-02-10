from pydantic import BaseModel, ConfigDict, Field


class JockeyCreateDTO(BaseModel):
    """DTO для создания жокея"""

    name: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)
    rating: int = Field(..., ge=0)


class JockeyDTO(BaseModel):
    """DTO жокея"""

    id: int
    name: str
    address: str
    age: int
    rating: int

    model_config = ConfigDict(from_attributes=True)
