from src.business.dto.participant_dto import ParticipantCreateDTO, ParticipantDTO
from src.data.uow import UnitOfWork


async def add_participant_with_result(
    uow: UnitOfWork, data: ParticipantCreateDTO
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
            data.race_id, data.jockey_id, data.horse_id
        )
        if existing:
            raise ValueError(
                f"Пара жокей-лошадь уже зарегистрирована в этом состязании"
            )

        # Создаем запись
        participant = await uow.participants.create(
            {
                "race_id": data.race_id,
                "jockey_id": data.jockey_id,
                "horse_id": data.horse_id,
                "place": data.place,
                "time_result": data.time_result,
            }
        )
        await uow.commit()
        return ParticipantDTO.model_validate(participant)
