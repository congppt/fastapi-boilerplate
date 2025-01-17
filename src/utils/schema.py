import ast
from datetime import datetime
from typing import Sequence, TypeVar, Generic, get_type_hints

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
    PositiveInt,
    NonNegativeInt,
)

from utils import PRIMITIVES
from utils.enums import FilterOption

T = TypeVar("T")
FILTER_TYPES = (*PRIMITIVES, datetime)


class PagingRequest(BaseModel):
    size: PositiveInt
    index: NonNegativeInt
    model_config = ConfigDict(from_attributes=True)


class QueryFilter(BaseModel, Generic[T]):
    attribute: str
    values: set = Field(min_length=1)
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
        type_hints = get_type_hints(obj=T)
        attr_type = type_hints.get(self.attribute, None)
        if not attr_type or attr_type not in FILTER_TYPES:
            raise ValueError(f"{self.attribute} is not a valid attribute")
        if self.option == FilterOption.BETWEEN and len(self.values) != 2:
            raise ValueError("BETWEEN filter only accepts 2 values")
        elif self.option == FilterOption.LIKE:
            if len(self.values) != 2:
                raise ValueError("LIKE filter only accepts 1 value")
            if attr_type is str:
                raise ValueError("LIKE filter only support <<str>> type attributes")
        if any(type(value) is attr_type for value in self.values):
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
    filters: str
    sort_by: str

    def resolve_filters(self, entity: type[T]):
        filters: list[QueryFilter[entity]] = []
        candidates = self.filters.split(sep=",")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            if len(metadata) < 3:
                raise ValueError(f"{candidate} is not a valid filter")
            if len(metadata) == 4 and metadata[2] != "NOT":
                raise ValueError("Filter option can only be negated by NOT keyword")
            values = set(ast.literal_eval(node_or_string=metadata[-1]))
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
        criteria: list[QuerySort[entity]] = []
        candidates = self.sort_by.split(",")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            if len(metadata) == 1:
                criteria.append(QuerySort[entity](attribute=metadata[0]))
                continue
            if metadata[1] not in {"ASC", "DESC"}:
                raise ValueError("Sorting order must be ASC or DESC")
            criteria.append(
                QuerySort[entity](attribute=metadata[0], asc=metadata[1] == "ASC")
            )
        return criteria


class PagingResponse(BaseModel):
    items: Sequence
    total_pages: NonNegativeInt
