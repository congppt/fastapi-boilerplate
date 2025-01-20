import ast
from datetime import datetime
import re
from typing import Any

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from pydantic_core import InitErrorDetails

from utils.enums import FilterOption

SORTABLE_TYPES = (str, int, float, datetime)
VALUE_REGEX = re.compile(
    r"^(?:\'[^\']*\'|\d+(?:\.\d+)?|\((?:\'[^\']*\'|\d+(?:\.\d+)?(?:\s*,\s*(?:\'[^\']*\'|\d+(?:\.\d+)?))*)\))$"
)


class PageRequest(BaseModel):
    size: int = Field(default=10, gt=0)
    index: int = Field(default=0, ge=0)


class EntityBasedCriteria(BaseModel):
    entity: type
    attribute: str = Field(default=...)

    @model_validator(mode="after")
    def validate_attribute(self):
        if not hasattr(self.entity, self.attribute):
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__,
                line_errors=[
                    InitErrorDetails(
                        type="value_error",
                        loc=("attribute",),
                        input=self.attribute,
                        ctx={
                            "error": ValueError(
                                f"{self.attribute} is not an attribute of {self.entity}"
                            )
                        },
                    )
                ],
            )
        return self


class FilterCriteria(EntityBasedCriteria):
    values: tuple = Field(min_length=1)
    option: FilterOption

    @field_validator("values")
    def validate(cls, v):
        typ = type(v[0])
        if any(type(value) is not typ for value in v):
            raise ValueError("All values must be of same type")
        return v

    @model_validator(mode="after")
    def validate_values(self):
        args_max = self.option.args_max()
        if args_max and len(self.values) > args_max:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__,
                line_errors=[
                    InitErrorDetails(
                        type="less_than",
                        loc=("values",),
                        input=self.values,
                        ctx={
                            "error": ValueError(
                                f"{self.option} filter accepts maximum {args_max} values"
                            )
                        },
                    )
                ],
            )
        args_min = self.option.args_min()
        if len(self.values) < args_min:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__,
                line_errors=[
                    InitErrorDetails(
                        type="greater_than",
                        loc=("values",),
                        input=self.values,
                        ctx={
                            "error": ValueError(
                                f"{self.option} filter accepts maximum {args_max} values"
                            )
                        },
                    )
                ],
            )
        return self

    def to_sql_filter(self) -> Any:
        raise NotImplementedError("Method is not implemented")


class FilterRequest(BaseModel):
    filters: str | None = Field(default=None)

    @field_validator("filters")
    def validate_filters(cls, v):
        candidates = v.split(sep=";") if v else []
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            if len(metadata) != 3:
                raise ValueError(
                    f"Invalid filter format. Expected '[attribute] [option] [value(s)]', got: '{candidate}'"
                )
            if not metadata[0]:
                raise ValueError("Attribute is required")
            options = {opt.value for opt in FilterOption}
            if metadata[-2] not in options:
                raise ValueError(
                    f"Invalid filter option: {metadata[-2]}. Must be one of [{', '.join(options)}]"
                )
            if not VALUE_REGEX.match(metadata[-1]):
                raise ValueError(
                    f"Invalid filter value(s): {metadata[-1]}. Expected a string, number, or a tuple of strings/numbers"
                )
        return v

    def resolve_filters(self, entity: type):
        filters: list[FilterCriteria] = []
        candidates = self.filters.split(sep=";") if self.filters else []
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            value = ast.literal_eval(node_or_string=metadata[-1])
            if isinstance(value, tuple | list | set):
                values = tuple(value)
            else:
                values = (value,)
            filters.append(
                FilterCriteria(
                    entity=entity,
                    attribute=metadata[0],
                    values=values,
                    option=FilterOption(value=metadata[-2]),
                )
            )
        return filters


class PriorityCriteria(EntityBasedCriteria):
    asc: bool = Field(default=True)

    def to_sql_priority(self) -> Any:
        raise NotImplementedError("Method is not implemented")


class PrioritizeRequest(BaseModel):
    priorities: str | None = Field(default=None)

    @field_validator("priorities")
    def validate_priorities(cls, v):
        candidates = v.split(sep=";") if v else []
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            if len(metadata) > 2:
                raise ValueError(
                    "Invalid priority format. Expected '[attribute] [ASC|DESC]'"
                )
            if not metadata[0]:
                raise ValueError("Attribute is required")
            if len(metadata) != 1 and metadata[1] not in {"ASC", "DESC"}:
                raise ValueError("Sorting order must be ASC or DESC")
        return v

    def resolve_priorities(self, entity: type):
        priorities: list[PriorityCriteria] = []
        candidates = self.priorities.split(sep=";") if self.priorities else []
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            priorities.append(
                PriorityCriteria(
                    entity=entity,
                    attribute=metadata[0],
                    asc=len(metadata) == 1 or metadata[1] == "ASC",
                )
            )
        return priorities


class QueryRequest(PageRequest, FilterRequest, PrioritizeRequest):
    pass
