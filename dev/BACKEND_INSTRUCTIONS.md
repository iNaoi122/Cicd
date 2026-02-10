# Backend RaceTracker - Инструкции для Claude Code

## Обзор проекта

Реализация backend части веб-приложения "RaceTracker" для управления информацией о скачках в клубе любителей скачек. Проект использует монорепозиторий и трехслойную архитектуру.

## Структура монорепозитория

```
racetracker/
├── backend/
│   ├── src/
│   │   ├── framework/          # Слой фреймворка (FastAPI)
│   │   ├── business/           # Слой бизнес-логики
│   │   ├── data/              # Слой доступа к данным
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic/               # Миграции БД
├── frontend/
└── docker-compose.yml
```

## Технологический стек

- **Python**: 3.11+
- **FastAPI**: веб-фреймворк
- **SQLAlchemy**: ORM для работы с PostgreSQL
- **Alembic**: миграции БД
- **Pydantic**: валидация данных и DTO
- **PostgreSQL**: база данных
- **pytest**: тестирование
- **Docker**: контейнеризация

## Архитектура: Трехслойная система

### Слой 1: Framework Layer (FastAPI)

**Расположение**: `backend/src/framework/`

**Ответственность**:
- HTTP endpoints (роутеры)
- Dependency Injection
- Обработка запросов/ответов
- Middleware (CORS, аутентификация)
- Валидация входных данных через Pydantic

**Структура**:
```
framework/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── races.py           # Эндпоинты состязаний
│   │   ├── jockeys.py         # Эндпоинты жокеев
│   │   ├── horses.py          # Эндпоинты лошадей
│   │   ├── owners.py          # Эндпоинты владельцев
│   │   └── participants.py    # Эндпоинты участников
├── dependencies.py            # DI контейнер
├── schemas.py                 # Pydantic модели запросов/ответов
└── middleware.py              # Middleware компоненты
```

**Pydantic схемы для API** (`framework/schemas.py`):
```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time
from typing import Optional

# Схемы для Race
class RaceBase(BaseModel):
    date: date = Field(..., description="Дата проведения состязания")
    time: time = Field(..., description="Время проведения")
    hippodrome: str = Field(..., min_length=1, max_length=200)
    name: Optional[str] = Field(None, max_length=200)

class RaceCreate(RaceBase):
    """Схема для создания состязания"""
    pass

class RaceResponse(RaceBase):
    """Схема ответа для состязания"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class ParticipantResultResponse(BaseModel):
    """Результат участника"""
    jockey_name: str
    horse_name: str
    place: int
    time_result: Optional[time] = None

class RaceWithParticipantsResponse(BaseModel):
    """Состязание с участниками и результатами"""
    race: RaceResponse
    participants: list[ParticipantResultResponse]

# Схемы для Jockey
class JockeyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: str = Field(..., min_length=1, max_length=500)
    age: int = Field(..., gt=0, lt=150)
    rating: int = Field(..., ge=0)

class JockeyCreate(JockeyBase):
    """Схема для создания жокея"""
    pass

class JockeyResponse(JockeyBase):
    """Схема ответа для жокея"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Схемы для Horse
class HorseBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., pattern="^(жеребец|кобыла|мерин)$")
    age: int = Field(..., gt=0, lt=50)
    owner_id: int = Field(..., gt=0)

class HorseCreate(HorseBase):
    """Схема для создания лошади"""
    pass

class HorseResponse(HorseBase):
    """Схема ответа для лошади"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Схемы для Owner
class OwnerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: str = Field(..., min_length=1, max_length=500)
    phone: str = Field(..., min_length=1, max_length=20)

class OwnerCreate(OwnerBase):
    """Схема для создания владельца"""
    pass

class OwnerResponse(OwnerBase):
    """Схема ответа для владельца"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Схемы для Participant
class ParticipantCreate(BaseModel):
    """Схема для добавления результата участника"""
    race_id: int = Field(..., gt=0)
    jockey_id: int = Field(..., gt=0)
    horse_id: int = Field(..., gt=0)
    place: int = Field(..., gt=0)
    time_result: Optional[time] = None

class ParticipantResponse(BaseModel):
    """Схема ответа для участника"""
    id: int
    race_id: int
    jockey_id: int
    horse_id: int
    place: int
    time_result: Optional[time]
    
    model_config = ConfigDict(from_attributes=True)
```

**Пример роутера** (`framework/api/v1/races.py`):
```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...dependencies import get_uow
from ...schemas import RaceCreate, RaceResponse, RaceWithParticipantsResponse
from business.race_operations import create_race, get_race_with_participants, list_races
from data.uow import UnitOfWork

router = APIRouter(prefix="/races", tags=["races"])

@router.post("/", response_model=RaceResponse, status_code=status.HTTP_201_CREATED)
async def create_race_endpoint(
    race_data: RaceCreate,
    uow: UnitOfWork = Depends(get_uow)
):
    """Создать новое состязание (Функция 2 из ТЗ)"""
    try:
        race = await create_race(uow, race_data)
        return race
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{race_id}", response_model=RaceWithParticipantsResponse)
async def get_race_endpoint(
    race_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """
    Получить состязание с участниками и результатами
    (Функция 1 из ТЗ)
    """
    race_data = await get_race_with_participants(uow, race_id)
    if not race_data:
        raise HTTPException(status_code=404, detail="Состязание не найдено")
    return race_data

@router.get("/", response_model=List[RaceResponse])
async def list_races_endpoint(
    skip: int = 0,
    limit: int = 100,
    uow: UnitOfWork = Depends(get_uow)
):
    """Получить список всех состязаний"""
    races = await list_races(uow, skip=skip, limit=limit)
    return races
```

**Dependency Injection** (`framework/dependencies.py`):
```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from data.database import async_session_maker
from data.uow import UnitOfWork

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получить сессию БД"""
    async with async_session_maker() as session:
        yield session

async def get_uow(session: AsyncSession = Depends(get_db)) -> UnitOfWork:
    """Получить Unit of Work"""
    return UnitOfWork(session)
```

---

### Слой 2: Business Layer (Бизнес-логика)

**Расположение**: `backend/src/business/`

**Ответственность**:
- Бизнес-правила и валидация
- Оркестрация операций над несколькими репозиториями
- **Чистая функциональная парадигма**
- Принимает зависимости (UoW) как параметры

**Структура**:
```
business/
├── __init__.py
├── race_operations.py        # Функции для работы с состязаниями
├── jockey_operations.py      # Функции для работы с жокеями
├── horse_operations.py       # Функции для работы с лошадьми
├── owner_operations.py       # Функции для работы с владельцами
├── participant_operations.py # Функции для работы с участниками
├── dto/                      # Data Transfer Objects (Pydantic)
│   ├── __init__.py
│   ├── race_dto.py
│   ├── jockey_dto.py
│   ├── horse_dto.py
│   ├── owner_dto.py
│   └── participant_dto.py
└── exceptions.py             # Бизнес-исключения
```

**Принципы реализации бизнес-логики**:
1. **Чистые функции**: каждая операция - это независимая функция
2. **Явная передача зависимостей**: UoW передается как первый параметр
3. **Без состояния**: функции не хранят состояние между вызовами
4. **Композируемость**: функции можно комбинировать
5. **Легкое тестирование**: можно мокировать UoW

**Pydantic DTO модели** (`business/dto/race_dto.py`):
```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time
from typing import Optional

class RaceCreateDTO(BaseModel):
    """DTO для создания состязания"""
    date: date
    time: time
    hippodrome: str
    name: Optional[str] = None

class RaceDTO(BaseModel):
    """DTO состязания"""
    id: int
    date: date
    time: time
    hippodrome: str
    name: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

class ParticipantResultDTO(BaseModel):
    """DTO результата участника"""
    jockey_name: str
    horse_name: str
    place: int
    time_result: Optional[time] = None

class RaceWithParticipantsDTO(BaseModel):
    """DTO состязания с участниками"""
    race: RaceDTO
    participants: list[ParticipantResultDTO]
```

**Бизнес-операции (функциональная парадигма)** (`business/race_operations.py`):
```python
from datetime import datetime
from typing import Optional
from data.uow import UnitOfWork
from business.dto.race_dto import RaceCreateDTO, RaceDTO, RaceWithParticipantsDTO, ParticipantResultDTO
from business.exceptions import RaceNotFoundError

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
    
    async with uow:
        race = await uow.races.create({
            "date": data.date,
            "time": data.time,
            "hippodrome": data.hippodrome,
            "name": data.name
        })
        await uow.commit()
        return RaceDTO.model_validate(race)

async def get_race_with_participants(
    uow: UnitOfWork,
    race_id: int
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
                time_result=p.time_result
            )
            for p in sorted_participants
        ]
        
        return RaceWithParticipantsDTO(
            race=RaceDTO.model_validate(race),
            participants=participants_dto
        )

async def list_races(
    uow: UnitOfWork,
    skip: int = 0,
    limit: int = 100
) -> list[RaceDTO]:
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
```

**Операции с жокеями** (`business/jockey_operations.py`):
```python
from typing import Optional
from data.uow import UnitOfWork
from business.dto.jockey_dto import JockeyCreateDTO, JockeyDTO

async def create_jockey(uow: UnitOfWork, data: JockeyCreateDTO) -> JockeyDTO:
    """
    Создать нового жокея
    
    Функция 3 из ТЗ: добавить нового жокея
    
    Args:
        uow: Unit of Work
        data: Данные жокея
        
    Returns:
        JockeyDTO: Созданный жокей
    """
    # Валидация бизнес-правил
    if data.age < 16:
        raise ValueError("Возраст жокея должен быть не менее 16 лет")
    
    if data.rating < 0:
        raise ValueError("Рейтинг не может быть отрицательным")
    
    async with uow:
        jockey = await uow.jockeys.create({
            "name": data.name,
            "address": data.address,
            "age": data.age,
            "rating": data.rating
        })
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
    uow: UnitOfWork,
    skip: int = 0,
    limit: int = 100
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
```

**Операции с участниками** (`business/participant_operations.py`):
```python
from data.uow import UnitOfWork
from business.dto.participant_dto import ParticipantCreateDTO, ParticipantDTO

async def add_participant_with_result(
    uow: UnitOfWork,
    data: ParticipantCreateDTO
) -> ParticipantDTO:
    """
    Добавить результат участника в состязании
    
    Функция 5 из ТЗ: добавить результаты прошедшего состязания
    
    Бизнес-правила:
    - Состязание должно существовать
    - Жокей должен существовать
    - Лошадь должна существовать
    - Место должно быть положительным числом
    - Пара жокей-лошадь не должна быть уже зарегистрирована в этом состязании
    
    Args:
        uow: Unit of Work
        data: Данные участника
        
    Returns:
        ParticipantDTO
        
    Raises:
        ValueError: Если бизнес-правила нарушены
    """
    async with uow:
        # Проверяем существование сущностей
        race = await uow.races.get_by_id(data.race_id)
        if not race:
            raise ValueError(f"Состязание с ID {data.race_id} не найдено")
        
        jockey = await uow.jockeys.get_by_id(data.jockey_id)
        if not jockey:
            raise ValueError(f"Жокей с ID {data.jockey_id} не найден")
        
        horse = await uow.horses.get_by_id(data.horse_id)
        if not horse:
            raise ValueError(f"Лошадь с ID {data.horse_id} не найдена")
        
        # Проверяем, что пара еще не участвует в этом состязании
        existing = await uow.participants.get_by_race_and_pair(
            data.race_id,
            data.jockey_id,
            data.horse_id
        )
        if existing:
            raise ValueError(
                f"Пара жокей-лошадь уже зарегистрирована в этом состязании"
            )
        
        # Создаем запись
        participant = await uow.participants.create({
            "race_id": data.race_id,
            "jockey_id": data.jockey_id,
            "horse_id": data.horse_id,
            "place": data.place,
            "time_result": data.time_result
        })
        await uow.commit()
        return ParticipantDTO.model_validate(participant)
```

**Pydantic DTO для жокеев** (`business/dto/jockey_dto.py`):
```python
from pydantic import BaseModel, Field, ConfigDict

class JockeyCreateDTO(BaseModel):
    """DTO для создания жокея"""
    name: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)
    rating: int = Field(..., ge=0)

class JockeyDTO(BaseModel):
    """DTO жокея"""
    id: int
    name: str
    address: str
    age: int
    rating: int
    
    model_config = ConfigDict(from_attributes=True)
```

**Pydantic DTO для лошадей** (`business/dto/horse_dto.py`):
```python
from pydantic import BaseModel, Field, ConfigDict

class HorseCreateDTO(BaseModel):
    """DTO для создания лошади"""
    nickname: str = Field(..., min_length=1)
    gender: str = Field(..., pattern="^(жеребец|кобыла|мерин)$")
    age: int = Field(..., gt=0)
    owner_id: int = Field(..., gt=0)

class HorseDTO(BaseModel):
    """DTO лошади"""
    id: int
    nickname: str
    gender: str
    age: int
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)
```

**Pydantic DTO для участников** (`business/dto/participant_dto.py`):
```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import time
from typing import Optional

class ParticipantCreateDTO(BaseModel):
    """DTO для создания участника"""
    race_id: int = Field(..., gt=0)
    jockey_id: int = Field(..., gt=0)
    horse_id: int = Field(..., gt=0)
    place: int = Field(..., gt=0)
    time_result: Optional[time] = None

class ParticipantDTO(BaseModel):
    """DTO участника"""
    id: int
    race_id: int
    jockey_id: int
    horse_id: int
    place: int
    time_result: Optional[time]
    
    model_config = ConfigDict(from_attributes=True)
```

**Исключения** (`business/exceptions.py`):
```python
class BusinessLogicError(Exception):
    """Базовое исключение бизнес-логики"""
    pass

class EntityNotFoundError(BusinessLogicError):
    """Сущность не найдена"""
    pass

class RaceNotFoundError(EntityNotFoundError):
    """Состязание не найдено"""
    pass

class JockeyNotFoundError(EntityNotFoundError):
    """Жокей не найден"""
    pass

class HorseNotFoundError(EntityNotFoundError):
    """Лошадь не найдена"""
    pass

class ValidationError(BusinessLogicError):
    """Ошибка валидации бизнес-правил"""
    pass
```

---

### Слой 3: Data Access Layer (Доступ к данным)

**Расположение**: `backend/src/data/`

**Ответственность**:
- Работа с БД через SQLAlchemy
- Паттерн Repository
- Unit of Work
- Модели SQLAlchemy

**Структура**:
```
data/
├── __init__.py
├── models.py                  # SQLAlchemy модели
├── database.py                # Настройка подключения к БД
├── repositories/
│   ├── __init__.py
│   ├── base.py               # Базовый репозиторий
│   ├── race_repository.py
│   ├── jockey_repository.py
│   ├── horse_repository.py
│   ├── owner_repository.py
│   └── participant_repository.py
└── uow.py                    # Unit of Work
```

**SQLAlchemy модели** (`data/models.py`):
```python
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Enum, Index
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class GenderEnum(enum.Enum):
    """Пол лошади"""
    STALLION = "жеребец"
    MARE = "кобыла"
    GELDING = "мерин"

class Race(Base):
    """Таблица состязаний"""
    __tablename__ = "races"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False)
    hippodrome = Column(String(200), nullable=False)
    name = Column(String(200), nullable=True)
    
    # Relationships
    participants = relationship("RaceParticipant", back_populates="race", lazy="selectin")

class Jockey(Base):
    """Таблица жокеев"""
    __tablename__ = "jockeys"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=False)
    age = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    
    # Relationships
    participations = relationship("RaceParticipant", back_populates="jockey")

class Owner(Base):
    """Таблица владельцев"""
    __tablename__ = "owners"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=False)
    phone = Column(String(20), nullable=False)
    
    # Relationships
    horses = relationship("Horse", back_populates="owner")

class Horse(Base):
    """Таблица лошадей"""
    __tablename__ = "horses"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(100), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    age = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    
    # Relationships
    owner = relationship("Owner", back_populates="horses")
    participations = relationship("RaceParticipant", back_populates="horse")

class RaceParticipant(Base):
    """
    Таблица участия в состязаниях
    Связывает состязание с парой жокей-лошадь и хранит результаты
    """
    __tablename__ = "race_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)
    jockey_id = Column(Integer, ForeignKey("jockeys.id"), nullable=False)
    horse_id = Column(Integer, ForeignKey("horses.id"), nullable=False)
    place = Column(Integer, nullable=False)  # Занятое место
    time_result = Column(Time, nullable=True)  # Время прохождения
    
    # Relationships
    race = relationship("Race", back_populates="participants")
    jockey = relationship("Jockey", back_populates="participations", lazy="selectin")
    horse = relationship("Horse", back_populates="participations", lazy="selectin")
    
    # Индексы для быстрого поиска
    __table_args__ = (
        Index('idx_race_place', 'race_id', 'place'),
        Index('idx_jockey_races', 'jockey_id'),
        Index('idx_horse_races', 'horse_id'),
    )
```

**Базовый репозиторий** (`data/repositories/base.py`):
```python
from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий с CRUD операциями"""
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def create(self, data: Dict[str, Any]) -> ModelType:
        """Создать новую запись"""
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Получить запись по ID"""
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Получить список записей"""
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def update(self, id: int, data: Dict[str, Any]) -> Optional[ModelType]:
        """Обновить запись"""
        instance = await self.get_by_id(id)
        if not instance:
            return None
        
        for key, value in data.items():
            setattr(instance, key, value)
        
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
    
    async def delete(self, id: int) -> bool:
        """Удалить запись"""
        instance = await self.get_by_id(id)
        if not instance:
            return False
        
        await self.session.delete(instance)
        await self.session.flush()
        return True
```

**Специализированный репозиторий** (`data/repositories/race_repository.py`):
```python
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from data.repositories.base import BaseRepository
from data.models import Race, RaceParticipant

class RaceRepository(BaseRepository[Race]):
    """Репозиторий для работы с состязаниями"""
    
    def __init__(self, session):
        super().__init__(Race, session)
    
    async def get_by_jockey_id(self, jockey_id: int) -> List[Race]:
        """
        Получить все состязания, в которых участвовал жокей
        Функция 6 из ТЗ
        """
        query = (
            select(Race)
            .join(Race.participants)
            .where(RaceParticipant.jockey_id == jockey_id)
            .order_by(Race.date.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().unique().all())
    
    async def get_by_horse_id(self, horse_id: int) -> List[Race]:
        """
        Получить все состязания, в которых участвовала лошадь
        Функция 7 из ТЗ
        """
        query = (
            select(Race)
            .join(Race.participants)
            .where(RaceParticipant.horse_id == horse_id)
            .order_by(Race.date.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().unique().all())
    
    async def get_with_participants(self, race_id: int) -> Optional[Race]:
        """
        Получить состязание со всеми участниками
        Функция 1 из ТЗ
        """
        query = (
            select(Race)
            .where(Race.id == race_id)
            .options(
                selectinload(Race.participants)
                .selectinload(RaceParticipant.jockey),
                selectinload(Race.participants)
                .selectinload(RaceParticipant.horse)
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
```

**Репозиторий участников** (`data/repositories/participant_repository.py`):
```python
from typing import Optional, List
from sqlalchemy import select, and_
from data.repositories.base import BaseRepository
from data.models import RaceParticipant

class ParticipantRepository(BaseRepository[RaceParticipant]):
    """Репозиторий для работы с участниками"""
    
    def __init__(self, session):
        super().__init__(RaceParticipant, session)
    
    async def get_by_race_id(
        self,
        race_id: int,
        with_relations: bool = False
    ) -> List[RaceParticipant]:
        """Получить всех участников состязания"""
        query = select(RaceParticipant).where(RaceParticipant.race_id == race_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_by_race_and_pair(
        self,
        race_id: int,
        jockey_id: int,
        horse_id: int
    ) -> Optional[RaceParticipant]:
        """Проверить, участвует ли пара в состязании"""
        query = select(RaceParticipant).where(
            and_(
                RaceParticipant.race_id == race_id,
                RaceParticipant.jockey_id == jockey_id,
                RaceParticipant.horse_id == horse_id
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
```

**Unit of Work** (`data/uow.py`):
```python
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from data.repositories import (
    RaceRepository,
    JockeyRepository,
    HorseRepository,
    OwnerRepository,
    ParticipantRepository
)

class UnitOfWork:
    """
    Unit of Work паттерн для управления транзакциями
    Обеспечивает атомарность операций и управление репозиториями
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self._races: Optional[RaceRepository] = None
        self._jockeys: Optional[JockeyRepository] = None
        self._horses: Optional[HorseRepository] = None
        self._owners: Optional[OwnerRepository] = None
        self._participants: Optional[ParticipantRepository] = None
    
    @property
    def races(self) -> RaceRepository:
        if self._races is None:
            self._races = RaceRepository(self.session)
        return self._races
    
    @property
    def jockeys(self) -> JockeyRepository:
        if self._jockeys is None:
            self._jockeys = JockeyRepository(self.session)
        return self._jockeys
    
    @property
    def horses(self) -> HorseRepository:
        if self._horses is None:
            self._horses = HorseRepository(self.session)
        return self._horses
    
    @property
    def owners(self) -> OwnerRepository:
        if self._owners is None:
            self._owners = OwnerRepository(self.session)
        return self._owners
    
    @property
    def participants(self) -> ParticipantRepository:
        if self._participants is None:
            self._participants = ParticipantRepository(self.session)
        return self._participants
    
    async def commit(self):
        """Зафиксировать транзакцию"""
        await self.session.commit()
    
    async def rollback(self):
        """Откатить транзакцию"""
        await self.session.rollback()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()
```

---

## Тестирование

**Пример unit-теста функции** (`tests/unit/test_race_operations.py`):
```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date, time
from business.race_operations import create_race, get_race_with_participants
from business.dto.race_dto import RaceCreateDTO

@pytest.mark.asyncio
async def test_create_race_success():
    """Тест успешного создания состязания"""
    # Arrange
    mock_uow = MagicMock()
    mock_race = MagicMock()
    mock_race.id = 1
    mock_race.date = date(2026, 3, 15)
    mock_race.time = time(14, 30)
    mock_race.hippodrome = "Московский ипподром"
    mock_race.name = "Весенний кубок"
    
    mock_uow.races.create = AsyncMock(return_value=mock_race)
    mock_uow.commit = AsyncMock()
    mock_uow.__aenter__ = AsyncMock(return_value=mock_uow)
    mock_uow.__aexit__ = AsyncMock()
    
    dto = RaceCreateDTO(
        date=date(2026, 3, 15),
        time=time(14, 30),
        hippodrome="Московский ипподром",
        name="Весенний кубок"
    )
    
    # Act
    result = await create_race(mock_uow, dto)
    
    # Assert
    assert result.id == 1
    assert result.hippodrome == "Московский ипподром"
    mock_uow.races.create.assert_called_once()
    mock_uow.commit.assert_called_once()

@pytest.mark.asyncio
async def test_create_race_past_date_fails():
    """Тест проверки бизнес-правила: дата не может быть в прошлом"""
    # Arrange
    mock_uow = MagicMock()
    mock_uow.__aenter__ = AsyncMock(return_value=mock_uow)
    mock_uow.__aexit__ = AsyncMock()
    
    dto = RaceCreateDTO(
        date=date(2020, 1, 1),  # Прошедшая дата
        time=time(14, 30),
        hippodrome="Московский ипподром"
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="прошлом"):
        await create_race(mock_uow, dto)
```

---

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY backend/src ./src
COPY backend/alembic ./alembic
COPY backend/alembic.ini .

# Переменные окружения
ENV PYTHONPATH=/app
ENV DATABASE_URL=postgresql+asyncpg://user:password@db:5432/racetracker

# Запуск миграций и приложения
CMD alembic upgrade head && \
    uvicorn src.main:app --host 0.0.0.0 --port 8000
```

---

## Основной файл приложения

**main.py**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from framework.api.v1 import races, jockeys, horses, owners, participants

app = FastAPI(
    title="RaceTracker API",
    description="API для управления информацией о скачках",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(races.router, prefix="/api/v1")
app.include_router(jockeys.router, prefix="/api/v1")
app.include_router(horses.router, prefix="/api/v1")
app.include_router(owners.router, prefix="/api/v1")
app.include_router(participants.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## Функции из ТЗ - Mapping

1. **Показать список жокеев и лошадей для каждого состязания с местами**
   - Endpoint: `GET /api/v1/races/{race_id}`
   - Function: `get_race_with_participants(uow, race_id)`
   - Repository: `RaceRepository.get_with_participants()`

2. **Добавить новое состязание**
   - Endpoint: `POST /api/v1/races`
   - Function: `create_race(uow, data)`
   - Repository: `RaceRepository.create()`

3. **Добавить нового жокея**
   - Endpoint: `POST /api/v1/jockeys`
   - Function: `create_jockey(uow, data)`
   - Repository: `JockeyRepository.create()`

4. **Добавить новую лошадь**
   - Endpoint: `POST /api/v1/horses`
   - Function: `create_horse(uow, data)`
   - Repository: `HorseRepository.create()`

5. **Добавить результаты состязания**
   - Endpoint: `POST /api/v1/participants`
   - Function: `add_participant_with_result(uow, data)`
   - Repository: `ParticipantRepository.create()`

6. **Показать список состязаний жокея**
   - Endpoint: `GET /api/v1/jockeys/{jockey_id}/races`
   - Function: `get_jockey_races(uow, jockey_id)`
   - Repository: `RaceRepository.get_by_jockey_id()`

7. **Показать список состязаний лошади**
   - Endpoint: `GET /api/v1/horses/{horse_id}/races`
   - Function: `get_horse_races(uow, horse_id)`
   - Repository: `RaceRepository.get_by_horse_id()`

---

## Requirements.txt

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
alembic==1.13.1
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

---

## Важные замечания

1. **Функциональная парадигма в Business Layer**: все операции - это чистые функции, принимающие UoW как параметр
2. **Pydantic DTO**: все DTO реализованы через Pydantic BaseModel с валидацией
3. **Слои изолированы**: Framework → Business → Data (строгая иерархия зависимостей)
4. **Легкое тестирование**: функции легко тестировать с мокированием UoW
5. **Repository + UoW**: обеспечивает транзакционность
6. **Async/await**: производительность через асинхронность
