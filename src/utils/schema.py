from abc import abstractmethod
import ast
from datetime import datetime
from typing import Any, Sequence, TypeVar, Generic, get_type_hints

from pydantic import BaseModel, Field, field_validator, model_validator

from utils import PRIMITIVES
from utils.enums import FilterOption

T = TypeVar("T")
FILTER_TYPES = (*PRIMITIVES, datetime)
SORT_TYPES = (*PRIMITIVES, datetime)


class PageResponse(BaseModel):
    items: Sequence
    total_pages: int = Field(ge=0)


class PageRequest(BaseModel):
    size: int = Field(default=10, gt=0)
    index: int = Field(default=0, ge=0)


class EntityBasedCriteria(BaseModel):
    entity: type
    attribute: str = Field(default=...)


class FilterCriteria(EntityBasedCriteria):
    values: tuple = Field(min_length=1)
    option: FilterOption
    negate: bool

    @field_validator("values")
    def values_validate(cls, v):
        typ = type(v[0])
        if typ not in FILTER_TYPES:
            raise ValueError(f"{typ} is not a valid filter type")
        if any(type(item) is not typ for item in v):
            raise ValueError("All queryvalues must have the same type")
        return v

    @model_validator(mode="after")
    def validate(self):
        wrap_attr_type = get_type_hints(self.entity).get(self.attribute, None)
        if (
            not wrap_attr_type
            or (attr_type := wrap_attr_type.__args__[0]) not in FILTER_TYPES
        ):
            raise ValueError(f"{self.attribute} is not a filterable attribute of {self.entity}")
        args_max = self.option.args_max()
        if len(self.values) > args_max:
            raise ValueError(
                f"{self.option} filter only accepts maximum {args_max} values"
            )
        args_min = self.option.args_min()
        if len(self.values) < args_min:
            raise ValueError(
                f"{self.option} filter only accepts minimum {args_min} values"
            )
        if self.option == FilterOption.LIKE:
            if attr_type is str:
                raise ValueError("LIKE filter only support <<str>> type attributes")
        if any(type(value) is not attr_type for value in self.values):
            raise ValueError("All values must have the same type as attributes")
        return self

    @abstractmethod
    def to_sql_filter(self) -> Any:
        pass


class FilterRequest(BaseModel):
    filters: str | None

    def resolve_filters(self, entity: type[T]):
        filters: list[FilterCriteria[entity]] = []
        candidates = self.filters.split(sep=";") if self.filters else []
        try:
            for candidate in candidates:
                metadata = candidate.split(sep=" ", maxsplit=3)
                if len(metadata) < 3:
                    raise ValueError(f"{candidate} is not a valid filter")
                if len(metadata) == 4 and metadata[2] != "NOT":
                    raise ValueError("Filter option can only be negated by NOT keyword")
                values = tuple(ast.literal_eval(node_or_string=metadata[-1]))
                filters.append(
                    FilterCriteria(
                        entity=entity,
                        attribute=metadata[0],
                        values=values,
                        option=FilterOption(value=metadata[-2]),
                        negate=len(metadata) == 4,
                    )
                )
        except ValueError as e:
            raise e
        return filters


class SortCriteria(EntityBasedCriteria):
    asc: bool = Field(default=True)

    @model_validator(mode="after")
    def validate(self):
        wrap_attr_type = get_type_hints(self.entity).get(self.attribute, None)
        if not wrap_attr_type or wrap_attr_type.__args__[0] not in SORT_TYPES:
            raise ValueError(f"{self.attribute} is not a valid sorting attribute")
        return self

    @abstractmethod
    def to_sql_priority(self) -> Any:
        pass


class SortRequest(BaseModel):
    priorities: str | None

    def resolve_sort_by(self, entity: type[T]):
        priorities: list[SortCriteria[entity]] = []
        candidates = self.priorities.split(";") if self.priorities else []
        try:
            for candidate in candidates:
                metadata = candidate.split(sep=" ", maxsplit=1)
                if len(metadata) == 1:
                    priorities.append(
                        SortCriteria(entity=entity, attribute=metadata[0])
                    )
                    continue
                if metadata[1] not in {"ASC", "DESC"}:
                    raise ValueError("Sorting order must be ASC or DESC")
                priorities.append(
                    SortCriteria(
                        entity=entity, attribute=metadata[0], asc=metadata[1] == "ASC"
                    )
                )
        except ValueError as e:
            raise e
        return priorities


class QueryRequest(PageRequest, FilterRequest, SortRequest):
    pass
