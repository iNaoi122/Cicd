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
