"""
E2E тесты для всех API эндпоинтов.
Используют httpx.AsyncClient + FastAPI TestClient подход.
"""

from datetime import date, time

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import Base
from src.framework.dependencies import get_db
from src.main import app


@pytest_asyncio.fixture
async def client():
    """Создать тестовый HTTP-клиент с изолированной БД в памяти."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    test_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with test_session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()


# ============================================================
# Races
# ============================================================


@pytest.mark.asyncio
async def test_create_race(client: AsyncClient):
    """POST /api/v1/races/ — создание состязания."""
    response = await client.post(
        "/api/v1/races/",
        json={
            "date": "2026-06-15",
            "time": "14:30:00",
            "hippodrome": "Московский ипподром",
            "name": "Весенний кубок",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["date"] == "2026-06-15"
    assert data["time"] == "14:30:00"
    assert data["hippodrome"] == "Московский ипподром"
    assert data["name"] == "Весенний кубок"


@pytest.mark.asyncio
async def test_create_race_without_name(client: AsyncClient):
    """POST /api/v1/races/ — создание без необязательного поля name."""
    response = await client.post(
        "/api/v1/races/",
        json={
            "date": "2026-07-01",
            "time": "10:00:00",
            "hippodrome": "Петербургский ипподром",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] is None


@pytest.mark.asyncio
async def test_create_race_past_date(client: AsyncClient):
    """POST /api/v1/races/ — дата в прошлом должна вернуть 400."""
    response = await client.post(
        "/api/v1/races/",
        json={
            "date": "2020-01-01",
            "time": "14:30:00",
            "hippodrome": "Московский ипподром",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_race_missing_field(client: AsyncClient):
    """POST /api/v1/races/ — отсутствие обязательного поля → 422."""
    response = await client.post(
        "/api/v1/races/",
        json={"date": "2026-06-15", "time": "14:30:00"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_races(client: AsyncClient):
    """GET /api/v1/races/ — получение списка состязаний."""
    # Создаём два состязания
    await client.post(
        "/api/v1/races/",
        json={
            "date": "2026-06-15",
            "time": "14:30:00",
            "hippodrome": "Ипподром 1",
        },
    )
    await client.post(
        "/api/v1/races/",
        json={
            "date": "2026-07-20",
            "time": "15:00:00",
            "hippodrome": "Ипподром 2",
        },
    )

    response = await client.get("/api/v1/races/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_race_by_id(client: AsyncClient):
    """GET /api/v1/races/{id} — получение состязания с участниками."""
    create_resp = await client.post(
        "/api/v1/races/",
        json={
            "date": "2026-06-15",
            "time": "14:30:00",
            "hippodrome": "Московский ипподром",
            "name": "Кубок",
        },
    )
    race_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/races/{race_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["race"]["id"] == race_id
    assert data["race"]["hippodrome"] == "Московский ипподром"
    assert data["participants"] == []


@pytest.mark.asyncio
async def test_get_race_not_found(client: AsyncClient):
    """GET /api/v1/races/999 — несуществующее состязание → 404."""
    response = await client.get("/api/v1/races/999")
    assert response.status_code == 404


# ============================================================
# Owners
# ============================================================


@pytest.mark.asyncio
async def test_create_owner(client: AsyncClient):
    """POST /api/v1/owners/ — создание владельца."""
    response = await client.post(
        "/api/v1/owners/",
        json={
            "name": "Иван Петров",
            "address": "Москва, ул. Парковая 5",
            "phone": "+7-900-123-45-67",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Иван Петров"


@pytest.mark.asyncio
async def test_list_owners(client: AsyncClient):
    """GET /api/v1/owners/ — список владельцев."""
    await client.post(
        "/api/v1/owners/",
        json={"name": "Владелец 1", "address": "Адрес 1", "phone": "111"},
    )
    await client.post(
        "/api/v1/owners/",
        json={"name": "Владелец 2", "address": "Адрес 2", "phone": "222"},
    )

    response = await client.get("/api/v1/owners/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_jockeys(client: AsyncClient):
    """GET /api/v1/jockeys/ — список жокеев."""
    await client.post(
        "/api/v1/jockeys/",
        json={"name": "Жокей 1", "address": "Адрес", "age": 20, "rating": 5},
    )

    response = await client.get("/api/v1/jockeys/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_get_jockey_by_id(client: AsyncClient):
    """GET /api/v1/jockeys/{id} — получение жокея по ID."""
    create_resp = await client.post(
        "/api/v1/jockeys/",
        json={"name": "Жокей", "address": "Адрес", "age": 25, "rating": 7},
    )
    jockey_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/jockeys/{jockey_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Жокей"
