import math

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.schema import PagingRequest, PagingResponse


async def apaging(query: Select[tuple], page: PagingRequest, db: AsyncSession) -> PagingResponse:
    """
    Executes given query and return paging result.
    ``query`` parameter should not be chained with ``limit()`` and ``offset()`` to avoid wrong counting.
    """
    count_query = select(func.count()).where(query.whereclause)
    count = await db.scalar(count_query)
    total_pages = math.ceil(count / page.size)
    page_query = query.offset(page.index * page.size).limit(page.size + 1)
    items = (await db.execute(page_query)).tuples().all()
    return PagingResponse(items=items, total_pages=total_pages)
