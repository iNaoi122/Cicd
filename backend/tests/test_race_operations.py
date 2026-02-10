from datetime import date, time

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.business.dto.horse_dto import HorseCreateDTO
from src.business.dto.jockey_dto import JockeyCreateDTO
from src.business.dto.owner_dto import OwnerCreateDTO
from src.business.dto.participant_dto import ParticipantCreateDTO
from src.business.dto.race_dto import RaceCreateDTO
from src.business.operations.horse_operations import create_horse
from src.business.operations.jockey_operations import create_jockey
from src.business.operations.owner_operations import create_owner
from src.business.operations.participant_operations import add_participant_with_result
from src.business.operations.race_operations import (
    create_race,
    get_horse_races,
    get_jockey_races,
    get_race_with_participants,
    list_races,
)
from src.data.uow import UnitOfWork


@pytest.mark.asyncio
async def test_create_race_success(async_session: AsyncSession):
    """Тест успешного создания состязания"""
    uow = UnitOfWork(async_session)

    dto = RaceCreateDTO(
        date=date(2026, 3, 15),
        time=time(14, 30),
        hippodrome="Московский ипподром",
        name="Весенний кубок",
    )

    result = await create_race(uow, dto)

    assert result.id is not None
    assert result.hippodrome == "Московский ипподром"
    assert result.name == "Весенний кубок"
    assert result.date == date(2026, 3, 15)
    assert result.time == time(14, 30)


@pytest.mark.asyncio
async def test_create_race_past_date_fails(async_session: AsyncSession):
    """Тест проверки бизнес-правила: дата не может быть в прошлом"""
    uow = UnitOfWork(async_session)

    dto = RaceCreateDTO(
        date=date(2020, 1, 1), time=time(14, 30), hippodrome="Московский ипподром"
    )

    with pytest.raises(ValueError, match="прошлом"):
        await create_race(uow, dto)


@pytest.mark.asyncio
async def test_get_race_with_participants_success(async_session: AsyncSession):
    """Тест получения состязания с участниками"""
    uow = UnitOfWork(async_session)

    # Создаем владельца
    owner_dto = OwnerCreateDTO(
        name="Иван Петров", address="Москва, ул. Парковая 5", phone="+7-900-123-45-67"
    )
    owner = await create_owner(uow, owner_dto)

    # Создаем жокея
    jockey_dto = JockeyCreateDTO(
        name="Алексей Смирнов", address="Москва, ул. Спортивная 10", age=25, rating=8
    )
    jockey = await create_jockey(uow, jockey_dto)

    # Создаем лошадь
    horse_dto = HorseCreateDTO(
        nickname="Гром", gender="жеребец", age=5, owner_id=owner.id
    )
    horse = await create_horse(uow, horse_dto)

    # Создаем состязание
    race_dto = RaceCreateDTO(
        date=date(2026, 3, 15),
        time=time(14, 30),
        hippodrome="Московский ипподром",
        name="Весенний кубок",
    )
    race = await create_race(uow, race_dto)

    # Добавляем участника
    participant_dto = ParticipantCreateDTO(
        race_id=race.id,
        jockey_id=jockey.id,
        horse_id=horse.id,
        place=1,
        time_result=time(2, 30),
    )
    await add_participant_with_result(uow, participant_dto)

    # Получаем состязание с участниками
    result = await get_race_with_participants(uow, race.id)

    assert result is not None
    assert result.race.id == race.id
    assert len(result.participants) == 1
    assert result.participants[0].jockey_name == "Алексей Смирнов"
    assert result.participants[0].horse_name == "Гром"
    assert result.participants[0].place == 1


@pytest.mark.asyncio
async def test_create_race_with_empty_hippodrome_fails(async_session: AsyncSession):
    """Тест валидации пустого названия ипподрома"""
    uow = UnitOfWork(async_session)

    dto = RaceCreateDTO(
        date=date(2026, 3, 15), time=time(14, 30), hippodrome="", name="Весенний кубок"
    )

    with pytest.raises(ValueError):
        await create_race(uow, dto)


@pytest.mark.asyncio
async def test_list_races_success(async_session: AsyncSession):
    """Тест получения списка состязаний"""
    uow = UnitOfWork(async_session)

    # Создаем несколько состязаний
    race1 = await create_race(
        uow,
        RaceCreateDTO(
            date=date(2026, 3, 15),
            time=time(14, 30),
            hippodrome="Московский ипподром",
            name="Весенний кубок",
        ),
    )

    race2 = await create_race(
        uow,
        RaceCreateDTO(
            date=date(2026, 4, 20),
            time=time(15, 0),
            hippodrome="Петербургский ипподром",
            name="Летний приз",
        ),
    )

    # Получаем список
    result = await list_races(uow)

    assert len(result) >= 2
    assert any(r.id == race1.id for r in result)
    assert any(r.id == race2.id for r in result)


@pytest.mark.asyncio
async def test_list_races_with_pagination(async_session: AsyncSession):
    """Тест получения списка состязаний с пагинацией"""
    uow = UnitOfWork(async_session)

    # Создаем состязания
    for i in range(5):
        await create_race(
            uow,
            RaceCreateDTO(
                date=date(2026, 3, 15 + i),
                time=time(14, 30),
                hippodrome=f"Ипподром {i}",
                name=f"Состязание {i}",
            ),
        )

    # Получаем с пагинацией
    result_page1 = await list_races(uow, skip=0, limit=2)
    result_page2 = await list_races(uow, skip=2, limit=2)

    assert len(result_page1) == 2
    assert len(result_page2) == 2
    assert result_page1[0].id != result_page2[0].id


@pytest.mark.asyncio
async def test_get_jockey_races_success(async_session: AsyncSession):
    """Тест получения состязаний жокея"""
    uow = UnitOfWork(async_session)

    # Создаем владельца, жокея и лошадь
    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    jockey = await create_jockey(
        uow, JockeyCreateDTO(name="Алексей Смирнов", address="Москва", age=25, rating=8)
    )

    horse = await create_horse(
        uow, HorseCreateDTO(nickname="Гром", gender="жеребец", age=5, owner_id=owner.id)
    )

    # Создаем состязания
    race1 = await create_race(
        uow,
        RaceCreateDTO(
            date=date(2026, 3, 15), time=time(14, 30), hippodrome="Московский ипподром"
        ),
    )

    race2 = await create_race(
        uow,
        RaceCreateDTO(
            date=date(2026, 4, 20),
            time=time(15, 0),
            hippodrome="Петербургский ипподром",
        ),
    )

    # Добавляем жокея в оба состязания
    await add_participant_with_result(
        uow,
        ParticipantCreateDTO(
            race_id=race1.id, jockey_id=jockey.id, horse_id=horse.id, place=1
        ),
    )

    await add_participant_with_result(
        uow,
        ParticipantCreateDTO(
            race_id=race2.id, jockey_id=jockey.id, horse_id=horse.id, place=2
        ),
    )

    # Получаем состязания жокея
    result = await get_jockey_races(uow, jockey.id)

    assert len(result) == 2
    assert any(r.id == race1.id for r in result)
    assert any(r.id == race2.id for r in result)


@pytest.mark.asyncio
async def test_get_horse_races_success(async_session: AsyncSession):
    """Тест получения состязаний лошади"""
    uow = UnitOfWork(async_session)

    # Создаем владельца, жокея и лошадь
    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    jockey = await create_jockey(
        uow, JockeyCreateDTO(name="Алексей Смирнов", address="Москва", age=25, rating=8)
    )

    horse = await create_horse(
        uow, HorseCreateDTO(nickname="Гром", gender="жеребец", age=5, owner_id=owner.id)
    )

    # Создаем состязания
    race1 = await create_race(
        uow,
        RaceCreateDTO(
            date=date(2026, 3, 15), time=time(14, 30), hippodrome="Московский ипподром"
        ),
    )

    race2 = await create_race(
        uow,
        RaceCreateDTO(
            date=date(2026, 4, 20),
            time=time(15, 0),
            hippodrome="Петербургский ипподром",
        ),
    )

    # Добавляем лошадь в оба состязания
    await add_participant_with_result(
        uow,
        ParticipantCreateDTO(
            race_id=race1.id, jockey_id=jockey.id, horse_id=horse.id, place=1
        ),
    )

    await add_participant_with_result(
        uow,
        ParticipantCreateDTO(
            race_id=race2.id, jockey_id=jockey.id, horse_id=horse.id, place=2
        ),
    )

    # Получаем состязания лошади
    result = await get_horse_races(uow, horse.id)

    assert len(result) == 2
    assert any(r.id == race1.id for r in result)
    assert any(r.id == race2.id for r in result)


@pytest.mark.asyncio
async def test_get_jockey_races_nonexistent_jockey_fails(async_session: AsyncSession):
    """Тест получения состязаний несуществующего жокея"""
    uow = UnitOfWork(async_session)

    with pytest.raises(ValueError, match="не найден"):
        await get_jockey_races(uow, 999)


@pytest.mark.asyncio
async def test_get_horse_races_nonexistent_horse_fails(async_session: AsyncSession):
    """Тест получения состязаний несуществующей лошади"""
    uow = UnitOfWork(async_session)

    with pytest.raises(ValueError, match="не найдена"):
        await get_horse_races(uow, 999)
