from datetime import datetime
from typing import Sequence, TypeVar, Generic, Literal, Annotated, Any

from pydantic import (BaseModel,
                      Field,
                      ConfigDict,
                      field_validator,
                      model_validator,
                      PositiveInt,
                      NonNegativeInt, conset)

from utils import PRIMITIVES

T = TypeVar('T')
FILTER_TYPES = (*PRIMITIVES, datetime)
class PagingRequest(BaseModel):
    size: PositiveInt
    index: NonNegativeInt
    model_config = ConfigDict(from_attributes=True)

class QueryFilter(BaseModel, Generic[T]):
    attribute: Annotated[str, Field(...)]
    values: conset(Any, min_length=1)
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
    def validate(self):
        if self.options == 'BETWEEN' and len(self.values) != 2:
            raise ValueError('BETWEEN filter only accepts 2 values')
        attr = getattr(T, self.attribute, None)
        if not attr or type(attr) not in FILTER_TYPES:
            raise ValueError(f'{attr} is not a valid attribute')


class QueryRequest(PagingRequest):
    filters: str

class PagingResponse:
    def __init__(self,
                 items: Sequence,
                 total_pages: int,
                 has_next: bool):
        self.items = items
        self.total_pages = total_pages
        self.has_next = has_next