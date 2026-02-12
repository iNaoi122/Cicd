"""
Падающий тест: проверяет метод promote_jockey, который намеренно
вызывает NotImplementedError (метод не реализован в репозитории).

Ожидаемое поведение при ИСПРАВЛЕНИИ: тест должен начать проходить
после реализации метода update в репозитории жокеев.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.business.dto.jockey_dto import JockeyCreateDTO
from src.business.operations.jockey_operations import create_jockey, promote_jockey
from src.data.uow import UnitOfWork


@pytest.mark.asyncio
async def test_promote_jockey_fails(async_session: AsyncSession):
    """
    ПАДАЮЩИЙ ТЕСТ.

    Вызывает promote_jockey, который бросает NotImplementedError —
    метод update не реализован в репозитории.

    Этот тест намеренно провалится: pytest.raises ожидает успешного
    выполнения, но функция всегда кидает NotImplementedError.
    """
    uow = UnitOfWork(async_session)

    jockey = await create_jockey(
        uow,
        JockeyCreateDTO(name="Тестовый Жокей", address="Москва", age=20, rating=5.0),
    )

    # Ожидаем успешного возврата DTO — но функция бросает NotImplementedError.
    # Тест УПАДЁТ с: NotImplementedError: Метод promote_jockey не реализован
    result = await promote_jockey(uow, jockey.id, bonus_rating=2.0)
    assert result.rating == 7.0
