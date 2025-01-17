from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User
from db.queries import apaging, sql_filters, sql_sort_by
from user.schema import UserCreateRequest
from utils.crypto import hash
from utils.schema import QueryRequest


async def acreate_user(request: UserCreateRequest, db: AsyncSession):
    password = hash(value=request.password)
    user = User(password=password, **request.model_dump())
    db.add(instance=user)
    await db.commit()
    return user


async def aget_users(db: AsyncSession, request: QueryRequest):
    filters = request.resolve_filters(entity=User)
    priorities = request.resolve_sort_by(entity=User)
    filters = sql_filters(filters=filters)
    priorities = sql_sort_by(priorities=priorities)
    query = select(User).where(*filters).order_by(*priorities)
    return await apaging(query=query, page=request, db=db)
