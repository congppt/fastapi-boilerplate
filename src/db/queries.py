import math
from typing import TypeVar

from sqlalchemy import Select, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped

from utils.enums import FilterOption
from utils.schema import PageRequest, PageResponse, FilterCriteria, SortCriteria


async def apaging(query: Select[tuple], page: PageRequest, db: AsyncSession):
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
    return PageResponse(items=items, total_pages=total_pages)


TEntity = TypeVar("TEntity", bound=DeclarativeBase)


def to_sql_filter(self: FilterCriteria):
    """Convert the QueryFilter to a SQLAlchemy filter expression.

    Returns:
        SQLAlchemy filter expression based on the filter option and values
    """
    column: Mapped = getattr(self.entity, self.attribute)
    operations = {
        FilterOption.BETWEEN: lambda: column.between(
            cleft=self.values[0], cright=self.values[1]
        ),
        FilterOption.IN: lambda: column.in_(other=self.values),
        FilterOption.LIKE: lambda: column.ilike(other=self.values[0]),
        FilterOption.LT: lambda: column < self.values[0],
        FilterOption.GT: lambda: column > self.values[0],
        FilterOption.LTE: lambda: column <= self.values[0],
        FilterOption.GTE: lambda: column >= self.values[0],
    }
    return operations[self.option]()


"""Monkey patch the QueryFilter class to add the to_sql_filter method"""
FilterCriteria.to_sql_filter = to_sql_filter


def to_sql_priority(self: SortCriteria):
    order = asc if self.asc else desc
    return order(column=getattr(self.entity, self.attribute))


"""Monkey patch the QuerySort class to add the to_sql_priority method"""
SortCriteria.to_sql_priority = to_sql_priority
