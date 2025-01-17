from enum import IntEnum, StrEnum


class Weekday(IntEnum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


class FunctionType(IntEnum):
    READ = 0
    WRITE = 1
    DELETE = 2


class FilterOption(StrEnum):
    IN = "IN"
    BETWEEN = "BETWEEN"
    LIKE = "LIKE"
