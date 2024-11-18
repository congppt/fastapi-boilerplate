from typing import Annotated

from pydantic import BaseModel, conset, Field

from utils.enums import Weekday


class CronSchedule(BaseModel):
    minute: Annotated[int, Field(ge=0, le=59)]
    hour: Annotated[int, Field(ge=0, le=23)]
    day: Annotated[int, Field(ge=1, le=31)]
    months: conset(Annotated[int, Field(ge=1, le=12)])
    days_of_week: conset(Annotated[Weekday, Field(ge=1, le=7)])
