from datetime import datetime
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
    NOT_IN = "NOT_IN"
    BETWEEN = "BETWEEN"
    NOT_BETWEEN = "NOT_BETWEEN"
    LIKE = "LIKE"
    NOT_LIKE = "NOT_LIKE"
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="

    def args_max(self):
        return {
            FilterOption.BETWEEN: 2,
            FilterOption.NOT_BETWEEN: 2,
            FilterOption.IN: None,
            FilterOption.NOT_IN: None,
            FilterOption.LIKE: 1,
            FilterOption.NOT_LIKE: 1,
            FilterOption.LT: 1,
            FilterOption.GT: 1,
            FilterOption.LTE: 1,
            FilterOption.GTE: 1,
        }[self]

    def args_min(self):
        return {
            FilterOption.BETWEEN: 2,
            FilterOption.NOT_BETWEEN: 2,
            FilterOption.IN: 1,
            FilterOption.NOT_IN: 1,
            FilterOption.LIKE: 1,
            FilterOption.NOT_LIKE: 1,
            FilterOption.LT: 1,
            FilterOption.GT: 1,
            FilterOption.LTE: 1,
            FilterOption.GTE: 1,
        }[self]

    def supported_types(self):
        return {
            FilterOption.IN: (
                list,
                tuple,
            ),
            FilterOption.NOT_IN: (list, tuple),
            FilterOption.LIKE: (str,),
            FilterOption.NOT_LIKE: (str,),
            FilterOption.BETWEEN: (list, tuple),
            FilterOption.NOT_BETWEEN: (list, tuple),
            FilterOption.LT: (int, float, str, datetime),
            FilterOption.GT: (int, float, str, datetime),
            FilterOption.LTE: (int, float, str, datetime),
            FilterOption.GTE: (int, float, str, datetime),
        }[self]
