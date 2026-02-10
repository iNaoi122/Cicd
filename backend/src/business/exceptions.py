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
