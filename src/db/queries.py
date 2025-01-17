import math
from typing import TypeVar

from sqlalchemy import Column, Select, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from utils.enums import FilterOption
from utils.schema import PagingRequest, PagingResponse, QueryFilter, QuerySort


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

TEntity = TypeVar("TEntity", bound=DeclarativeBase)
async def sql_filters(filters: list[QueryFilter[TEntity]]):
    conditions = []
    for filter in filters:
        column: Column = getattr(TEntity, filter.attribute)
        expression = None
        if filter.option == FilterOption.BETWEEN:
            expression = column.between(cleft=filter.values[0], cright=filter.values[1])
        elif filter.option == FilterOption.IN:
            expression = column.in_(other=filter.values)
        elif filter.option == FilterOption.LIKE:
            expression = column.ilike(other=filter.values[0])
        elif filter.option == FilterOption.LT:
            expression = column < filter.values[0]
        elif filter.option == FilterOption.GT:
            expression = column > filter.values[0]
        elif filter.option == FilterOption.LTE:
            expression = column <= filter.values[0]
        elif filter.option == FilterOption.GTE:
            expression = column >= filter.values[0]
        conditions.append(expression)
    return conditions

async def sql_sort_by(priorities: list[QuerySort[TEntity]]):
    criteria = []
    for priority in priorities:
        order = asc if priority.asc else desc
        criteria.append(order(column=getattr(TEntity, priority.attribute)))
    return criteria