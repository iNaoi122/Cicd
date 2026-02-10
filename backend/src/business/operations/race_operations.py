from datetime import datetime
from typing import Optional

from src.business.dto.race_dto import (
    ParticipantResultDTO,
    RaceCreateDTO,
    RaceDTO,
    RaceWithParticipantsDTO,
)
from src.data.uow import UnitOfWork


async def create_race(uow: UnitOfWork, data: RaceCreateDTO) -> RaceDTO:
    """
    Создать новое состязание

    Бизнес-правила:
    - Дата состязания не может быть в прошлом
    - Название ипподрома обязательно

    Args:
        uow: Unit of Work для доступа к репозиториям
        data: Данные для создания состязания

    Returns:
        RaceDTO: Созданное состязание

    Raises:
        ValueError: Если бизнес-правила нарушены
    """
    # Валидация бизнес-правил
    if data.date < datetime.now().date():
        raise ValueError("Дата состязания не может быть в прошлом")

    if not data.hippodrome or not data.hippodrome.strip():
        raise ValueError("Название ипподрома не может быть пустым")

    async with uow:
        race = await uow.races.create(
            {
                "date": data.date,
                "time": data.time,
                "hippodrome": data.hippodrome,
                "name": data.name,
            }
        )
        await uow.commit()
        return RaceDTO.model_validate(race)


async def get_race_with_participants(
    uow: UnitOfWork, race_id: int
) -> Optional[RaceWithParticipantsDTO]:
    """
    Получить состязание с участниками и результатами

    Функция 1 из ТЗ: для каждого состязания показать список
    жокеев и лошадей с указанием занятых ими мест

    Args:
        uow: Unit of Work
        race_id: ID состязания

    Returns:
        RaceWithParticipantsDTO или None если не найдено
    """
    async with uow:
        race = await uow.races.get_with_participants(race_id)
        if not race:
            return None

        # Сортируем участников по занятому месту
        sorted_participants = sorted(race.participants, key=lambda p: p.place)

        # Формируем DTO
        participants_dto = [
            ParticipantResultDTO(
                jockey_name=p.jockey.name,
                horse_name=p.horse.nickname,
                place=p.place,
                time_result=p.time_result,
            )
            for p in sorted_participants
        ]

        return RaceWithParticipantsDTO(
            race=RaceDTO.model_validate(race), participants=participants_dto
        )


async def list_races(uow: UnitOfWork, skip: int = 0, limit: int = 100) -> list[RaceDTO]:
    """
    Получить список всех состязаний

    Args:
        uow: Unit of Work
        skip: Количество записей для пропуска
        limit: Максимальное количество записей

    Returns:
        Список RaceDTO
    """
    async with uow:
        races = await uow.races.list(skip=skip, limit=limit)
        return [RaceDTO.model_validate(race) for race in races]


async def get_jockey_races(uow: UnitOfWork, jockey_id: int) -> list[RaceDTO]:
    """
    Получить список состязаний жокея

    Функция 6 из ТЗ: показать список состязаний каждого жокея

    Args:
        uow: Unit of Work
        jockey_id: ID жокея

    Returns:
        Список состязаний жокея

    Raises:
        ValueError: Если жокей не найден
    """
    async with uow:
        # Проверяем существование жокея
        jockey = await uow.jockeys.get_by_id(jockey_id)
        if not jockey:
            raise ValueError(f"Жокей с ID {jockey_id} не найден")

        # Получаем состязания через участие
        races = await uow.races.get_by_jockey_id(jockey_id)
        return [RaceDTO.model_validate(race) for race in races]


async def get_horse_races(uow: UnitOfWork, horse_id: int) -> list[RaceDTO]:
    """
    Получить список состязаний лошади

    Функция 7 из ТЗ: показать список состязаний каждой лошади

    Args:
        uow: Unit of Work
        horse_id: ID лошади

    Returns:
        Список состязаний лошади

    Raises:
        ValueError: Если лошадь не найдена
    """
    async with uow:
        horse = await uow.horses.get_by_id(horse_id)
        if not horse:
            raise ValueError(f"Лошадь с ID {horse_id} не найдена")

        races = await uow.races.get_by_horse_id(horse_id)
        return [RaceDTO.model_validate(race) for race in races]


async def validate_race_data(data: RaceCreateDTO) -> None:
    """
    Валидация данных состязания

    Пример вспомогательной функции для композиции

    Args:
        data: Данные состязания

    Raises:
        ValueError: Если данные невалидны
    """
    if data.date < datetime.now().date():
        raise ValueError("Дата состязания не может быть в прошлом")

    if not data.hippodrome.strip():
        raise ValueError("Название ипподрома не может быть пустым")
