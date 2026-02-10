import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.business.dto.horse_dto import HorseCreateDTO
from src.business.dto.owner_dto import OwnerCreateDTO
from src.business.operations.horse_operations import (
    create_horse,
    get_horse_by_id,
    list_horses,
)
from src.business.operations.owner_operations import create_owner
from src.data.uow import UnitOfWork


@pytest.mark.asyncio
async def test_create_horse_success(async_session: AsyncSession):
    """Тест успешного создания лошади"""
    uow = UnitOfWork(async_session)

    # Сначала создаем владельца
    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    # Создаем лошадь
    dto = HorseCreateDTO(nickname="Гром", gender="жеребец", age=5, owner_id=owner.id)

    result = await create_horse(uow, dto)

    assert result.id is not None
    assert result.nickname == "Гром"
    assert result.gender == "жеребец"
    assert result.age == 5
    assert result.owner_id == owner.id


@pytest.mark.asyncio
async def test_create_horse_nonexistent_owner_fails(async_session: AsyncSession):
    """Тест создания лошади с несуществующим владельцем"""
    uow = UnitOfWork(async_session)

    dto = HorseCreateDTO(
        nickname="Гром",
        gender="жеребец",
        age=5,
        owner_id=999,  # Несуществующий владелец
    )

    with pytest.raises(ValueError, match="не найден"):
        await create_horse(uow, dto)


@pytest.mark.asyncio
async def test_get_horse_by_id_success(async_session: AsyncSession):
    """Тест получения лошади по ID"""
    uow = UnitOfWork(async_session)

    # Создаем владельца и лошадь
    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    created = await create_horse(
        uow, HorseCreateDTO(nickname="Гром", gender="жеребец", age=5, owner_id=owner.id)
    )

    # Получаем лошадь
    result = await get_horse_by_id(uow, created.id)

    assert result is not None
    assert result.id == created.id
    assert result.nickname == "Гром"


@pytest.mark.asyncio
async def test_get_horse_by_id_not_found(async_session: AsyncSession):
    """Тест получения несуществующей лошади"""
    uow = UnitOfWork(async_session)

    result = await get_horse_by_id(uow, 999)

    assert result is None


@pytest.mark.asyncio
async def test_list_horses_success(async_session: AsyncSession):
    """Тест получения списка лошадей"""
    uow = UnitOfWork(async_session)

    # Создаем владельца и несколько лошадей
    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    horse1 = await create_horse(
        uow, HorseCreateDTO(nickname="Гром", gender="жеребец", age=5, owner_id=owner.id)
    )

    horse2 = await create_horse(
        uow, HorseCreateDTO(nickname="Ветра", gender="кобыла", age=4, owner_id=owner.id)
    )

    # Получаем список
    result = await list_horses(uow)

    assert len(result) >= 2
    assert any(h.id == horse1.id for h in result)
    assert any(h.id == horse2.id for h in result)


@pytest.mark.asyncio
async def test_list_horses_with_pagination(async_session: AsyncSession):
    """Тест получения списка лошадей с пагинацией"""
    uow = UnitOfWork(async_session)

    # Создаем владельца и лошадей
    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    for i in range(5):
        await create_horse(
            uow,
            HorseCreateDTO(
                nickname=f"Лошадь {i}", gender="жеребец", age=5, owner_id=owner.id
            ),
        )

    # Получаем с пагинацией
    result_page1 = await list_horses(uow, skip=0, limit=2)
    result_page2 = await list_horses(uow, skip=2, limit=2)

    assert len(result_page1) == 2
    assert len(result_page2) == 2
    assert result_page1[0].id != result_page2[0].id


@pytest.mark.asyncio
async def test_create_horse_with_invalid_gender_fails(async_session: AsyncSession):
    """Тест валидации пола лошади"""
    uow = UnitOfWork(async_session)

    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    # Попытка создания с невалидным полом - должна упасть на уровне Pydantic
    with pytest.raises(Exception):
        HorseCreateDTO(
            nickname="Гром",
            gender="слон",  # Невалидный пол
            age=5,
            owner_id=owner.id,
        )


@pytest.mark.asyncio
async def test_create_horse_mare_success(async_session: AsyncSession):
    """Тест создания кобылы"""
    uow = UnitOfWork(async_session)

    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    result = await create_horse(
        uow, HorseCreateDTO(nickname="Ветра", gender="кобыла", age=3, owner_id=owner.id)
    )

    assert result.gender == "кобыла"


@pytest.mark.asyncio
async def test_create_horse_gelding_success(async_session: AsyncSession):
    """Тест создания мерина"""
    uow = UnitOfWork(async_session)

    owner = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    result = await create_horse(
        uow, HorseCreateDTO(nickname="Боец", gender="мерин", age=6, owner_id=owner.id)
    )

    assert result.gender == "мерин"
