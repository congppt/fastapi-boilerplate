import ast
from datetime import datetime
from typing import Sequence, TypeVar, Generic, get_args, get_type_hints

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from utils import PRIMITIVES
from utils.enums import FilterOption

T = TypeVar("T")
FILTER_TYPES = (*PRIMITIVES, datetime)


class PagingRequest(BaseModel):
    size: int = Field(default=10, gt=0)
    index: int = Field(default=0, ge=0)
    model_config = ConfigDict(from_attributes=True)


class QueryFilter(BaseModel, Generic[T]):
    attribute: str
    values: tuple = Field(min_length=1)
    option: FilterOption
    negate: bool

    @field_validator("values")
    def values_validate(cls, v):
        typ = type(v[0])
        if typ not in FILTER_TYPES:
            raise ValueError(f"{typ} is not a valid filter type")
        if any(type(item) is typ for item in v):
            raise ValueError("Values must have the same type")
        return v

    @model_validator(mode="after")
    def validate(self):
        type_hints = get_type_hints(obj=get_args(tp=type(self))[0])
        attr_type = type_hints.get(self.attribute, None)
        if not attr_type or attr_type not in FILTER_TYPES:
            raise ValueError(f"{self.attribute} is not a valid attribute")
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


class QuerySort(BaseModel, Generic[T]):
    attribute: str = Field(default=...)
    asc: bool = Field(default=True)

    @model_validator(mode="after")
    def validate(self):
        attr = getattr(T, self.attribute, None)
        if not attr or type(attr) not in FILTER_TYPES:
            raise ValueError(f"{attr} is not a valid attribute")
        return self


class QueryRequest(PagingRequest):
    filters: str | None
    sort_by: str | None

    def resolve_filters(self, entity: type[T]):
        filters: list[QueryFilter[entity]] = []
        candidates = self.filters.split(sep=";") if self.filters else []
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            if len(metadata) < 3:
                raise ValueError(f"{candidate} is not a valid filter")
            if len(metadata) == 4 and metadata[2] != "NOT":
                raise ValueError("Filter option can only be negated by NOT keyword")
            values = tuple(ast.literal_eval(node_or_string=metadata[-1]))
            filters.append(
                QueryFilter[entity](
                    attribute=metadata[0],
                    values=values,
                    option=FilterOption(value=metadata[-2]),
                    negate=len(metadata) == 4,
                )
            )
        return filters

    def resolve_sort_by(self, entity: type[T]):
        priorities: list[QuerySort[entity]] = []
        candidates = self.sort_by.split(";") if self.sort_by else []
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            if len(metadata) == 1:
                priorities.append(QuerySort[entity](attribute=metadata[0]))
                continue
            if metadata[1] not in {"ASC", "DESC"}:
                raise ValueError("Sorting order must be ASC or DESC")
            priorities.append(
                QuerySort[entity](attribute=metadata[0], asc=metadata[1] == "ASC")
            )
        return priorities


class PagingResponse(BaseModel):
    items: Sequence
    total_pages: int = Field(ge=0)
