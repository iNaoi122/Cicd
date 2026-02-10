from typing import Optional

from src.business.dto.horse_dto import HorseCreateDTO, HorseDTO
from src.data.models import GenderEnum
from src.data.uow import UnitOfWork


async def create_horse(uow: UnitOfWork, data: HorseCreateDTO) -> HorseDTO:
    """
    Создать новую лошадь

    Функция 4 из ТЗ: добавить новую лошадь

    Args:
        uow: Unit of Work
        data: Данные лошади

    Returns:
        HorseDTO: Созданная лошадь

    Raises:
        ValueError: Если бизнес-правила нарушены
    """
    # Валидация существования владельца
    async with uow:
        owner = await uow.owners.get_by_id(data.owner_id)
        if not owner:
            raise ValueError(f"Владелец с ID {data.owner_id} не найден")

        horse = await uow.horses.create(
            {
                "nickname": data.nickname,
                "gender": GenderEnum(data.gender),
                "age": data.age,
                "owner_id": data.owner_id,
            }
        )
        await uow.commit()
        return HorseDTO.model_validate(horse)


async def get_horse_by_id(uow: UnitOfWork, horse_id: int) -> Optional[HorseDTO]:
    """
    Получить лошадь по ID

    Args:
        uow: Unit of Work
        horse_id: ID лошади

    Returns:
        HorseDTO или None
    """
    async with uow:
        horse = await uow.horses.get_by_id(horse_id)
        if not horse:
            return None
        return HorseDTO.model_validate(horse)


async def list_horses(
    uow: UnitOfWork, skip: int = 0, limit: int = 100
) -> list[HorseDTO]:
    """
    Получить список лошадей

    Args:
        uow: Unit of Work
        skip: Пропустить записей
        limit: Максимум записей

    Returns:
        Список HorseDTO
    """
    async with uow:
        horses = await uow.horses.list(skip=skip, limit=limit)
        return [HorseDTO.model_validate(h) for h in horses]
