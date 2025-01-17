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
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="

    def args_max(self):
        return {
            FilterOption.BETWEEN: 2,
            FilterOption.IN: None,
            FilterOption.LIKE: 1,
            FilterOption.LT: 1,
            FilterOption.GT: 1,
            FilterOption.LTE: 1,
            FilterOption.GTE: 1,
        }[self]

    def args_min(self):
        return {
            FilterOption.BETWEEN: 2,
            FilterOption.IN: 1,
            FilterOption.LIKE: 1,
            FilterOption.LT: 1,
            FilterOption.GT: 1,
            FilterOption.LTE: 1,
            FilterOption.GTE: 1,
        }[self]
