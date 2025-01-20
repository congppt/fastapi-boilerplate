import ast
from datetime import datetime
from typing import Any, TypeVar

from pydantic import BaseModel, Field, field_validator, model_validator

from utils.enums import FilterOption

T = TypeVar("T")
SORTABLE_TYPES = (str, int, float, datetime)


class PageRequest(BaseModel):
    size: int = Field(default=10, gt=0)
    index: int = Field(default=0, ge=0)


class EntityBasedCriteria(BaseModel):
    entity: type
    attribute: str = Field(default=...)

    @model_validator(mode="after")
    def validate_attribute(self):
        if not hasattr(self.entity, self.attribute):
            raise ValueError(f"{self.attribute} is not an attribute of {self.entity}")
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
            raise ValueError(f"{self.option} filter accepts maximum {args_max} values")
        args_min = self.option.args_min()
        if len(self.values) < args_min:
            raise ValueError(f"{self.option} filter accepts minimum {args_min} values")
        return self

    def to_sql_filter(self) -> Any:
        raise NotImplementedError("Method is not implemented")


class FilterRequest(BaseModel):
    filters: str | None = Field(default=None)

    def resolve_filters(self, entity: type[T]):
        filters: list[FilterCriteria] = []
        candidates = self.filters.split(sep=";") if self.filters else []
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            if len(metadata) < 3:
                raise ValueError(f"Filter missing arguments: {candidate}")
            try:
                value = ast.literal_eval(node_or_string=metadata[-1])
                if isinstance(value, dict):
                    raise ValueError()
            except Exception:
                raise ValueError(f"Invalid filter values: {metadata[-1]}")
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


class SortRequest(BaseModel):
    priorities: str | None = Field(default=None)

    def resolve_sort_by(self, entity: type[T]):
        priorities: list[PriorityCriteria] = []
        candidates = self.priorities.split(sep=";") if self.priorities else []
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            if len(metadata) == 1:
                priorities.append(
                    PriorityCriteria(entity=entity, attribute=metadata[0])
                )
                continue
            if metadata[1] not in {"ASC", "DESC"}:
                raise ValueError("Sorting order must be ASC or DESC")
            priorities.append(
                PriorityCriteria(
                    entity=entity, attribute=metadata[0], asc=metadata[1] == "ASC"
                )
            )
        return priorities


class QueryRequest(PageRequest, FilterRequest, SortRequest):
    pass
