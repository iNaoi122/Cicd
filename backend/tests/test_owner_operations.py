import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.business.dto.owner_dto import OwnerCreateDTO
from src.business.operations.owner_operations import (
    create_owner,
    get_owner_by_id,
    list_owners,
)
from src.data.uow import UnitOfWork


@pytest.mark.asyncio
async def test_create_owner_success(async_session: AsyncSession):
    """Тест успешного создания владельца"""
    uow = UnitOfWork(async_session)

    dto = OwnerCreateDTO(
        name="Иван Петров", address="Москва, ул. Парковая 5", phone="+7-900-123-45-67"
    )

    result = await create_owner(uow, dto)

    assert result.id is not None
    assert result.name == "Иван Петров"
    assert result.address == "Москва, ул. Парковая 5"
    assert result.phone == "+7-900-123-45-67"


@pytest.mark.asyncio
async def test_get_owner_by_id_success(async_session: AsyncSession):
    """Тест получения владельца по ID"""
    uow = UnitOfWork(async_session)

    # Создаем владельца
    created = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-000-00-00"),
    )

    # Получаем владельца
    result = await get_owner_by_id(uow, created.id)

    assert result is not None
    assert result.id == created.id
    assert result.name == "Иван Петров"


@pytest.mark.asyncio
async def test_get_owner_by_id_not_found(async_session: AsyncSession):
    """Тест получения несуществующего владельца"""
    uow = UnitOfWork(async_session)

    result = await get_owner_by_id(uow, 999)

    assert result is None


@pytest.mark.asyncio
async def test_list_owners_success(async_session: AsyncSession):
    """Тест получения списка владельцев"""
    uow = UnitOfWork(async_session)

    # Создаем несколько владельцев
    owner1 = await create_owner(
        uow,
        OwnerCreateDTO(name="Иван Петров", address="Москва", phone="+7-900-111-11-11"),
    )

    owner2 = await create_owner(
        uow,
        OwnerCreateDTO(
            name="Петр Иванов", address="Санкт-Петербург", phone="+7-900-222-22-22"
        ),
    )

    # Получаем список
    result = await list_owners(uow)

    assert len(result) >= 2
    assert any(o.id == owner1.id for o in result)
    assert any(o.id == owner2.id for o in result)


@pytest.mark.asyncio
async def test_list_owners_with_pagination(async_session: AsyncSession):
    """Тест получения списка владельцев с пагинацией"""
    uow = UnitOfWork(async_session)

    # Создаем владельцев
    for i in range(5):
        await create_owner(
            uow,
            OwnerCreateDTO(
                name=f"Владелец {i}",
                address=f"Город {i}",
                phone=f"+7-900-{i:03d}-{i:02d}-{i:02d}",
            ),
        )

    # Получаем с пагинацией
    result_page1 = await list_owners(uow, skip=0, limit=2)
    result_page2 = await list_owners(uow, skip=2, limit=2)

    assert len(result_page1) == 2
    assert len(result_page2) == 2
    assert result_page1[0].id != result_page2[0].id
