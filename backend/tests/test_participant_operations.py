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
from src.business.operations.race_operations import create_race
from src.data.uow import UnitOfWork


@pytest.mark.asyncio
async def test_add_participant_success(async_session: AsyncSession):
    """Тест успешного добавления участника"""
    uow = UnitOfWork(async_session)

    # Создаем владельца
    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    # Создаем жокея
    jockey = await create_jockey(
        uow, JockeyCreateDTO(name="Алексей", address="Москва", age=25, rating=8)
    )

    # Создаем лошадь
    horse = await create_horse(
        uow, HorseCreateDTO(nickname="Гром", gender="жеребец", age=5, owner_id=owner.id)
    )

    # Создаем состязание
    race = await create_race(
        uow,
        RaceCreateDTO(
            date=date(2026, 3, 15), time=time(14, 30), hippodrome="Московский ипподром"
        ),
    )

    # Добавляем участника
    result = await add_participant_with_result(
        uow,
        ParticipantCreateDTO(
            race_id=race.id,
            jockey_id=jockey.id,
            horse_id=horse.id,
            place=1,
            time_result=time(2, 30),
        ),
    )

    assert result.id is not None
    assert result.race_id == race.id
    assert result.jockey_id == jockey.id
    assert result.horse_id == horse.id
    assert result.place == 1


@pytest.mark.asyncio
async def test_add_participant_duplicate_fails(async_session: AsyncSession):
    """Тест: пара жокей-лошадь не может участвовать дважды"""
    uow = UnitOfWork(async_session)

    # Создаем владельца, жокея, лошадь, состязание
    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    jockey = await create_jockey(
        uow, JockeyCreateDTO(name="Алексей", address="Москва", age=25, rating=8)
    )

    horse = await create_horse(
        uow, HorseCreateDTO(nickname="Гром", gender="жеребец", age=5, owner_id=owner.id)
    )

    race = await create_race(
        uow,
        RaceCreateDTO(
            date=date(2026, 3, 15), time=time(14, 30), hippodrome="Московский ипподром"
        ),
    )

    # Добавляем первого участника
    await add_participant_with_result(
        uow,
        ParticipantCreateDTO(
            race_id=race.id, jockey_id=jockey.id, horse_id=horse.id, place=1
        ),
    )

    # Попытка добавить ту же пару - должна упасть
    with pytest.raises(ValueError, match="уже зарегистрирована"):
        await add_participant_with_result(
            uow,
            ParticipantCreateDTO(
                race_id=race.id, jockey_id=jockey.id, horse_id=horse.id, place=2
            ),
        )


@pytest.mark.asyncio
async def test_add_participant_nonexistent_race_fails(async_session: AsyncSession):
    """Тест: добавление участника в несуществующее состязание"""
    uow = UnitOfWork(async_session)

    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    jockey = await create_jockey(
        uow, JockeyCreateDTO(name="Алексей", address="Москва", age=25, rating=8)
    )

    horse = await create_horse(
        uow, HorseCreateDTO(nickname="Гром", gender="жеребец", age=5, owner_id=owner.id)
    )

    with pytest.raises(ValueError, match="не найдено"):
        await add_participant_with_result(
            uow,
            ParticipantCreateDTO(
                race_id=999, jockey_id=jockey.id, horse_id=horse.id, place=1
            ),
        )
