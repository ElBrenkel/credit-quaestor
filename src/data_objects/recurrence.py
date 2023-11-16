from enum import Enum, auto


class RecurrenceType(Enum):
    DAILY = 1
    WEEKLY = auto()
    MONTHLY = auto()
    YEARLY = auto()
