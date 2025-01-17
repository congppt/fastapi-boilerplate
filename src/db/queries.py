import math

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.schema import PagingRequest, PagingResponse


async def apaging(query: Select[tuple], page: PagingRequest, db: AsyncSession):
    """
    Executes given query and return paging result.
    ``query`` parameter should not be chained with ``limit()`` and ``offset()`` to avoid wrong counting.
    """
    count_query = select(func.count()).select_from(query.subquery())
    count = await db.scalar(statement=count_query)
    if not count:
        raise ValueError("Count query returned no result")
    total_pages = math.ceil(count / page.size)
    page_query = query.offset(offset=page.index * page.size).limit(limit=page.size + 1)
    items = (await db.execute(statement=page_query)).tuples().all()
    return PagingResponse(items=items, total_pages=total_pages)
