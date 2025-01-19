from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User
from db.queries import apaging
from user.schema import UserCreateRequest
from utils.crypto import hash
from utils.schema import QueryRequest


async def acreate_user(request: UserCreateRequest, db: AsyncSession):
    password = hash(value=request.password)
    user_data = request.model_dump()
    user_data["password"] = password
    user = User(**user_data)
    db.add(instance=user)
    await db.commit()
    await db.refresh(instance=user)
    return user


async def aget_users(db: AsyncSession, request: QueryRequest):
    filters = [
        filter.to_sql_filter() for filter in request.resolve_filters(entity=User)
    ]
    priorities = [
        priority.to_sql_priority() for priority in request.resolve_sort_by(entity=User)
    ]
    query = select(User).where(*filters).order_by(*priorities)
    return await apaging(query=query, page=request, db=db)
