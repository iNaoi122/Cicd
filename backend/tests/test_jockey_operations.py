import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from src.business.dto.jockey_dto import JockeyCreateDTO
from src.business.operations.jockey_operations import create_jockey, get_jockey_by_id
from src.data.uow import UnitOfWork


@pytest.mark.asyncio
async def test_create_jockey_success(async_session: AsyncSession):
    """Тест успешного создания жокея"""
    uow = UnitOfWork(async_session)

    dto = JockeyCreateDTO(
        name="Алексей Смирнов", address="Москва, ул. Спортивная 10", age=25, rating=8
    )

    result = await create_jockey(uow, dto)

    assert result.id is not None
    assert result.name == "Алексей Смирнов"
    assert result.age == 25
    assert result.rating == 8


@pytest.mark.asyncio
async def test_create_jockey_too_young_fails(async_session: AsyncSession):
    """Тест проверки минимального возраста жокея"""
    uow = UnitOfWork(async_session)

    dto = JockeyCreateDTO(
        name="Молодой жокей", address="Москва, ул. Спортивная 10", age=15, rating=5
    )

    with pytest.raises(ValueError, match="16 лет"):
        await create_jockey(uow, dto)


@pytest.mark.asyncio
async def test_create_jockey_negative_rating_fails(async_session: AsyncSession):
    """Тест проверки отрицательного рейтинга"""
    with pytest.raises(ValidationError):
        JockeyCreateDTO(
            name="Жокей", address="Москва, ул. Спортивная 10", age=25, rating=-5
        )


@pytest.mark.asyncio
async def test_get_jockey_by_id_success(async_session: AsyncSession):
    """Тест получения жокея по ID"""
    uow = UnitOfWork(async_session)

    # Создаем жокея
    dto = JockeyCreateDTO(
        name="Алексей Смирнов", address="Москва, ул. Спортивная 10", age=25, rating=8
    )
    created = await create_jockey(uow, dto)

    # Получаем жокея
    result = await get_jockey_by_id(uow, created.id)

    assert result is not None
    assert result.id == created.id
    assert result.name == "Алексей Смирнов"


@pytest.mark.asyncio
async def test_get_jockey_by_id_not_found(async_session: AsyncSession):
    """Тест получения несуществующего жокея"""
    uow = UnitOfWork(async_session)

    result = await get_jockey_by_id(uow, 999)

    assert result is None
