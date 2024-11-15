import math
from typing import Sequence

from pydantic import BaseModel, Field
from sqlalchemy import Select, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypeVar, Generic

T = TypeVar('T')

class PagingRequest(BaseModel):
    size: int | None = Field(ge=1)
    index: int = Field(0, ge=0)

class PagingResponse(Generic[T]):
    def __init__(self, items: Sequence[T], total_pages: int, has_next: bool):
        self.items = items
        self.total_pages = total_pages
        self.has_next = has_next
    @classmethod
    async def from_query(cls, db: AsyncSession, query: Select[tuple], page: PagingRequest) -> 'PagingResponse[T]':
        """
        Executes given query and return paging result.

        ``query`` parameter should not be chained with ``limit()`` and ``offset()`` to avoid wrong counting.
        """
        count_query = select(func.count()).where(query.whereclause)
        count = await db.scalar(count_query)
        total_pages = math.ceil(count / page.size)
        page_query = query.offset(page.index * page.size).limit(page.size + 1)
        items = (await db.execute(page_query)).tuples().all()
        has_next = len(items) > page.size
        items = items[:-1] if has_next else items
        return cls(items, total_pages, has_next)