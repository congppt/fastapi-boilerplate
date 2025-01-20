import math

from sqlalchemy import Select, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.enums import FilterOption
from utils.schema import PageRequest, FilterCriteria, PriorityCriteria


async def apaging(query: Select[tuple], page: PageRequest, db: AsyncSession):
    """
    Executes given query and return paging result.
    ``query`` parameter should not be chained with ``limit()`` and ``offset()`` to avoid wrong counting.
    """
    count_query = select(func.count()).select_from(query.subquery())
    count = await db.scalar(statement=count_query)
    if count is None:
        raise ValueError("Count query returned no result")
    total_pages = math.ceil(count / page.size)
    page_query = query.offset(offset=page.index * page.size).limit(limit=page.size)
    if len(query.column_descriptions) == 1:
        items = (await db.execute(statement=page_query)).scalars().all()
    else:
        items = (await db.execute(statement=page_query)).mappings().all()
    return {"items": items, "total_pages": total_pages}




def to_sql_filter(self: FilterCriteria):
    """Convert the QueryFilter to a SQLAlchemy filter expression.

    Returns:
        SQLAlchemy filter expression based on the filter option and values
    """
    column = getattr(self.entity, self.attribute)
    inner_type = column.type.python_type
    values = [inner_type(value) for value in self.values]
    operations = {
        FilterOption.BETWEEN: lambda: column.between(
            cleft=self.values[0], cright=values[1]
        ),
        FilterOption.NOT_BETWEEN: lambda: ~column.between(
            cleft=self.values[0], cright=values[1]
        ),
        FilterOption.IN: lambda: column.in_(other=values),
        FilterOption.NOT_IN: lambda: column.not_in(other=values),
        FilterOption.LIKE: lambda: column.ilike(other=values[0]),
        FilterOption.NOT_LIKE: lambda: column.not_ilike(other=values[0]),
        FilterOption.LT: lambda: column < values[0],
        FilterOption.GT: lambda: column > values[0],
        FilterOption.LTE: lambda: column <= values[0],
        FilterOption.GTE: lambda: column >= values[0],
    }
    return operations[self.option]()


"""Monkey patch the QueryFilter class to add the to_sql_filter method"""
FilterCriteria.to_sql_filter = to_sql_filter


def to_sql_priority(self: PriorityCriteria):
    priority = asc if self.asc else desc
    return priority(column=getattr(self.entity, self.attribute))


"""Monkey patch the QuerySort class to add the to_sql_priority method"""
PriorityCriteria.to_sql_priority = to_sql_priority
