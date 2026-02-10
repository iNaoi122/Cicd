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
async def test_get_owner_by_id(client: AsyncClient):
    """GET /api/v1/owners/{id} — получение владельца по ID."""
    create_resp = await client.post(
        "/api/v1/owners/",
        json={"name": "Иван", "address": "Москва", "phone": "123"},
    )
    owner_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/owners/{owner_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Иван"


@pytest.mark.asyncio
async def test_get_owner_not_found(client: AsyncClient):
    """GET /api/v1/owners/999 — несуществующий владелец → 404."""
    response = await client.get("/api/v1/owners/999")
    assert response.status_code == 404


# ============================================================
# Jockeys
# ============================================================


@pytest.mark.asyncio
async def test_create_jockey(client: AsyncClient):
    """POST /api/v1/jockeys/ — создание жокея."""
    response = await client.post(
        "/api/v1/jockeys/",
        json={
            "name": "Алексей Смирнов",
            "address": "Москва, ул. Спортивная 10",
            "age": 25,
            "rating": 8,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Алексей Смирнов"
    assert data["age"] == 25
    assert data["rating"] == 8


@pytest.mark.asyncio
async def test_create_jockey_underage(client: AsyncClient):
    """POST /api/v1/jockeys/ — жокей младше 16 лет → 400."""
    response = await client.post(
        "/api/v1/jockeys/",
        json={"name": "Молодой", "address": "Москва", "age": 15, "rating": 5},
    )
    assert response.status_code == 400


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


@pytest.mark.asyncio
async def test_get_jockey_not_found(client: AsyncClient):
    """GET /api/v1/jockeys/999 — 404."""
    response = await client.get("/api/v1/jockeys/999")
    assert response.status_code == 404


# ============================================================
# Horses
# ============================================================


@pytest.mark.asyncio
async def test_create_horse(client: AsyncClient):
    """POST /api/v1/horses/ — создание лошади."""
    # Сначала владелец
    owner_resp = await client.post(
        "/api/v1/owners/",
        json={"name": "Владелец", "address": "Адрес", "phone": "123"},
    )
    owner_id = owner_resp.json()["id"]

    response = await client.post(
        "/api/v1/horses/",
        json={
            "nickname": "Гром",
            "gender": "жеребец",
            "age": 5,
            "owner_id": owner_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["nickname"] == "Гром"
    assert data["gender"] == "жеребец"


@pytest.mark.asyncio
async def test_create_horse_invalid_gender(client: AsyncClient):
    """POST /api/v1/horses/ — невалидный пол → 422."""
    owner_resp = await client.post(
        "/api/v1/owners/",
        json={"name": "Владелец", "address": "Адрес", "phone": "123"},
    )
    owner_id = owner_resp.json()["id"]

    response = await client.post(
        "/api/v1/horses/",
        json={
            "nickname": "Лошадь",
            "gender": "invalid",
            "age": 5,
            "owner_id": owner_id,
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_horse_nonexistent_owner(client: AsyncClient):
    """POST /api/v1/horses/ — несуществующий владелец → 400."""
    response = await client.post(
        "/api/v1/horses/",
        json={
            "nickname": "Лошадь",
            "gender": "кобыла",
            "age": 3,
            "owner_id": 999,
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_horses(client: AsyncClient):
    """GET /api/v1/horses/ — список лошадей."""
    owner_resp = await client.post(
        "/api/v1/owners/",
        json={"name": "Владелец", "address": "Адрес", "phone": "123"},
    )
    owner_id = owner_resp.json()["id"]
    await client.post(
        "/api/v1/horses/",
        json={"nickname": "Молния", "gender": "кобыла", "age": 4, "owner_id": owner_id},
    )

    response = await client.get("/api/v1/horses/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_get_horse_by_id(client: AsyncClient):
    """GET /api/v1/horses/{id} — получение лошади по ID."""
    owner_resp = await client.post(
        "/api/v1/owners/",
        json={"name": "Владелец", "address": "Адрес", "phone": "123"},
    )
    owner_id = owner_resp.json()["id"]
    create_resp = await client.post(
        "/api/v1/horses/",
        json={"nickname": "Звезда", "gender": "кобыла", "age": 6, "owner_id": owner_id},
    )
    horse_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/horses/{horse_id}")
    assert response.status_code == 200
    assert response.json()["nickname"] == "Звезда"


@pytest.mark.asyncio
async def test_get_horse_not_found(client: AsyncClient):
    """GET /api/v1/horses/999 — 404."""
    response = await client.get("/api/v1/horses/999")
    assert response.status_code == 404


# ============================================================
# Participants
# ============================================================


async def _create_full_setup(client: AsyncClient):
    """Вспомогательная функция: создать владельца, жокея, лошадь и состязание."""
    owner_resp = await client.post(
        "/api/v1/owners/",
        json={"name": "Владелец", "address": "Адрес", "phone": "123"},
    )
    owner_id = owner_resp.json()["id"]

    jockey_resp = await client.post(
        "/api/v1/jockeys/",
        json={"name": "Жокей", "address": "Адрес", "age": 25, "rating": 7},
    )
    jockey_id = jockey_resp.json()["id"]

    horse_resp = await client.post(
        "/api/v1/horses/",
        json={"nickname": "Гром", "gender": "жеребец", "age": 5, "owner_id": owner_id},
    )
    horse_id = horse_resp.json()["id"]

    race_resp = await client.post(
        "/api/v1/races/",
        json={
            "date": "2026-08-01",
            "time": "12:00:00",
            "hippodrome": "Тестовый ипподром",
        },
    )
    race_id = race_resp.json()["id"]

    return owner_id, jockey_id, horse_id, race_id


@pytest.mark.asyncio
async def test_add_participant(client: AsyncClient):
    """POST /api/v1/participants/ — добавить результат участника."""
    _, jockey_id, horse_id, race_id = await _create_full_setup(client)

    response = await client.post(
        "/api/v1/participants/",
        json={
            "race_id": race_id,
            "jockey_id": jockey_id,
            "horse_id": horse_id,
            "place": 1,
            "time_result": "02:15:00",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["place"] == 1
    assert data["race_id"] == race_id
    assert data["jockey_id"] == jockey_id
    assert data["horse_id"] == horse_id


@pytest.mark.asyncio
async def test_add_participant_nonexistent_race(client: AsyncClient):
    """POST /api/v1/participants/ — несуществующее состязание → 400."""
    _, jockey_id, horse_id, _ = await _create_full_setup(client)

    response = await client.post(
        "/api/v1/participants/",
        json={
            "race_id": 999,
            "jockey_id": jockey_id,
            "horse_id": horse_id,
            "place": 1,
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_add_participant_duplicate(client: AsyncClient):
    """POST /api/v1/participants/ — дублирование пары жокей-лошадь → 400."""
    _, jockey_id, horse_id, race_id = await _create_full_setup(client)

    # Первый раз — ОК
    resp1 = await client.post(
        "/api/v1/participants/",
        json={
            "race_id": race_id,
            "jockey_id": jockey_id,
            "horse_id": horse_id,
            "place": 1,
        },
    )
    assert resp1.status_code == 201

    # Повторно — ошибка
    resp2 = await client.post(
        "/api/v1/participants/",
        json={
            "race_id": race_id,
            "jockey_id": jockey_id,
            "horse_id": horse_id,
            "place": 2,
        },
    )
    assert resp2.status_code == 400


# ============================================================
# Cross-entity: состязание с участниками, состязания жокея/лошади
# ============================================================


@pytest.mark.asyncio
async def test_race_with_participants(client: AsyncClient):
    """GET /api/v1/races/{id} — состязание с результатами участников."""
    _, jockey_id, horse_id, race_id = await _create_full_setup(client)

    await client.post(
        "/api/v1/participants/",
        json={
            "race_id": race_id,
            "jockey_id": jockey_id,
            "horse_id": horse_id,
            "place": 1,
            "time_result": "02:15:00",
        },
    )

    response = await client.get(f"/api/v1/races/{race_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["participants"]) == 1
    p = data["participants"][0]
    assert p["jockey_name"] == "Жокей"
    assert p["horse_name"] == "Гром"
    assert p["place"] == 1
    assert p["time_result"] == "02:15:00"


@pytest.mark.asyncio
async def test_jockey_races(client: AsyncClient):
    """GET /api/v1/jockeys/{id}/races — состязания жокея."""
    _, jockey_id, horse_id, race_id = await _create_full_setup(client)

    await client.post(
        "/api/v1/participants/",
        json={
            "race_id": race_id,
            "jockey_id": jockey_id,
            "horse_id": horse_id,
            "place": 1,
        },
    )

    response = await client.get(f"/api/v1/jockeys/{jockey_id}/races")
    assert response.status_code == 200
    races = response.json()
    assert len(races) == 1
    assert races[0]["hippodrome"] == "Тестовый ипподром"


@pytest.mark.asyncio
async def test_horse_races(client: AsyncClient):
    """GET /api/v1/horses/{id}/races — состязания лошади."""
    _, jockey_id, horse_id, race_id = await _create_full_setup(client)

    await client.post(
        "/api/v1/participants/",
        json={
            "race_id": race_id,
            "jockey_id": jockey_id,
            "horse_id": horse_id,
            "place": 2,
        },
    )

    response = await client.get(f"/api/v1/horses/{horse_id}/races")
    assert response.status_code == 200
    races = response.json()
    assert len(races) == 1
    assert races[0]["hippodrome"] == "Тестовый ипподром"


@pytest.mark.asyncio
async def test_jockey_races_not_found(client: AsyncClient):
    """GET /api/v1/jockeys/999/races — несуществующий жокей → 404."""
    response = await client.get("/api/v1/jockeys/999/races")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_horse_races_not_found(client: AsyncClient):
    """GET /api/v1/horses/999/races — несуществующая лошадь → 404."""
    response = await client.get("/api/v1/horses/999/races")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """GET /health — проверка работоспособности."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
