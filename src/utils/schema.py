from datetime import datetime
from typing import Sequence, TypeVar, Generic, Literal, Annotated, Any

from pydantic import BaseModel, Field, ConfigDict, conlist, field_validator, model_validator
from pydantic.v1 import PositiveInt, NonNegativeInt

from utils import PRIMITIVES

T = TypeVar('T')
FILTER_TYPES = (*PRIMITIVES, datetime)
class PagingRequest(BaseModel):
    size: PositiveInt
    index: NonNegativeInt
    model_config = ConfigDict(from_attributes=True)

class QueryFilter(BaseModel):
    attribute: Annotated[str, Field(...)]
    values: conlist(Any, min_length=1, unique_items=True)
    options: Literal['IN', 'BETWEEN']
    negate: bool

    @field_validator('values')
    def values_validate(cls, v):    # noqa
        typ = type(v[0])
        if typ not in FILTER_TYPES:
            raise ValueError(f'{typ} is not a valid filter type')
        if any(type(item) != typ for item in v):
            raise ValueError('Values must have the same type')
        return v

    @model_validator(mode='after')
    def options_validate(self):
        if self.options is 'BETWEEN' and len(self.values) != 2:
            raise ValueError('BETWEEN filter only accepts 2 values')


class QueryRequest(PagingRequest):
    filters: str

class PagingResponse(Generic[T]):
    def __init__(self,
                 items: Sequence[T],
                 total_pages: int,
                 has_next: bool):
        self.items = items
        self.total_pages = total_pages
        self.has_next = has_next