from pydantic import BaseModel, ConfigDict, Field


class OwnerCreateDTO(BaseModel):
    """DTO для создания владельца"""

    name: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)


class OwnerDTO(BaseModel):
    """DTO владельца"""

    id: int
    name: str
    address: str
    phone: str

    model_config = ConfigDict(from_attributes=True)
