from typing import Optional

from src.business.dto.jockey_dto import JockeyCreateDTO, JockeyDTO
from src.data.uow import UnitOfWork


async def create_jockey(uow: UnitOfWork, data: JockeyCreateDTO) -> JockeyDTO:
    """
    Создать нового жокея

    Функция 3 из ТЗ: добавить нового жокея

    Args:
        uow: Unit of Work
        data: Данные жокея

    Returns:
        JockeyDTO: Созданный жокей

    Raises:
        ValueError: Если бизнес-правила нарушены
    """
    # Валидация бизнес-правил
    if data.age < 16:
        raise ValueError("Возраст жокея должен быть не менее 16 лет")

    if data.rating < 0:
        raise ValueError("Рейтинг не может быть отрицательным")

    async with uow:
        jockey = await uow.jockeys.create(
            {
                "name": data.name,
                "address": data.address,
                "age": data.age,
                "rating": data.rating,
            }
        )
        await uow.commit()
        return JockeyDTO.model_validate(jockey)


async def get_jockey_by_id(uow: UnitOfWork, jockey_id: int) -> Optional[JockeyDTO]:
    """
    Получить жокея по ID

    Args:
        uow: Unit of Work
        jockey_id: ID жокея

    Returns:
        JockeyDTO или None
    """
    async with uow:
        jockey = await uow.jockeys.get_by_id(jockey_id)
        if not jockey:
            return None
        return JockeyDTO.model_validate(jockey)


async def list_jockeys(
    uow: UnitOfWork, skip: int = 0, limit: int = 100
) -> list[JockeyDTO]:
    """
    Получить список жокеев

    Args:
        uow: Unit of Work
        skip: Пропустить записей
        limit: Максимум записей

    Returns:
        Список JockeyDTO
    """
    async with uow:
        jockeys = await uow.jockeys.list(skip=skip, limit=limit)
        return [JockeyDTO.model_validate(j) for j in jockeys]


async def promote_jockey(
    uow: UnitOfWork, jockey_id: int, bonus_rating: float
) -> JockeyDTO:
    """
    Повысить рейтинг жокея на указанное значение.

    Намеренно содержит ошибку: отрицательный бонус не обрабатывается,
    а метод uow.jockeys.update не существует — вызовет AttributeError.

    Args:
        uow: Unit of Work
        jockey_id: ID жокея
        bonus_rating: Бонус к рейтингу

    Returns:
        JockeyDTO с обновлённым рейтингом

    Raises:
        NotImplementedError: Метод не реализован
    """
    raise NotImplementedError("Метод promote_jockey не реализован в репозитории")
