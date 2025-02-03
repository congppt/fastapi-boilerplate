import ast
from datetime import datetime
import re
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_core import InitErrorDetails, PydanticCustomError

from utils.enums import FilterOption

T = TypeVar("T")
SORTABLE_TYPES = (str, int, float, datetime)
VALUE_REGEX = re.compile(
    pattern=r"^(?:\'[^\']*\'|\d+(?:\.\d+)?|\((?:\'[^\']*\'|\d+(?:\.\d+)?(?:\s*,\s*(?:\'[^\']*\'|\d+(?:\.\d+)?))*)\))$"
)


class PageRequest(BaseModel):
    size: int = Field(default=10, gt=0)
    index: int = Field(default=0, ge=0)


class EntityBasedCriteria(BaseModel):
    entity: type
    attribute: str = Field(default=...)


class FilterCriteria(EntityBasedCriteria):
    values: tuple = Field(min_length=1)
    option: FilterOption

    def to_sql_filter(self) -> Any:
        raise NotImplementedError("Method is not implemented")


class FilterRequest(BaseModel, Generic[T]):
    filters: str | None = Field(default=None)

    @field_validator("filters")
    def validate_filters(cls, v: str | None) -> str | None:
        if not v:  # Early return for None/empty
            return v
        candidates = v.split(sep=";")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            if len(metadata) != 3:
                raise ValueError(
                    f"Invalid filter format. Expected '[attribute] [option] [values]', got: '{candidate}'"
                )
            attribute, option_str, value_str = metadata
            # Validate attribute
            if not attribute:
                raise ValueError("Attribute required")
            entity_type = cls.__pydantic_generic_metadata__["args"][0]
            if not hasattr(entity_type, attribute):
                raise ValueError(
                    f"'{attribute}' is not an attribute of {entity_type.__name__}"
                )
            # Validate option
            if option_str not in {opt.value for opt in FilterOption}:
                raise ValueError(
                    f"Invalid option '{option_str}'. Must be one of: {', '.join(opt.value for opt in FilterOption)}"
                )
            # Validate value format and type
            if not VALUE_REGEX.match(string=value_str):
                raise ValueError(
                    "Expected a string, number, or tuple of strings/numbers"
                )
            # Parse and validate values
            value = ast.literal_eval(node_or_string=value_str)
            values = (
                tuple(value) if isinstance(value, (tuple, list, set)) else (value,)
            )
            option = FilterOption(value=option_str)
            if option.args_max() and len(values) > option.args_max():
                raise ValueError(f"Maximum {option.args_max()} values allowed")
            if len(values) < option.args_min():
                raise ValueError(f"Minimum {option.args_min()} values required")

            if not all(isinstance(x, type(values[0])) for x in values):
                raise ValueError("All values must be of same type")
        return v

    def resolve_filters(self):
        """Resolves filter string into FilterCriteria objects.

        Returns:
            list[FilterCriteria]: List of parsed filter criteria
        """
        if not self.filters:
            return []
        filters: list[FilterCriteria] = []
        candidates = self.filters.split(sep=";")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            value = ast.literal_eval(node_or_string=metadata[-1])
            if isinstance(value, tuple | list | set):
                values = tuple(value)
            else:
                values = (value,)
            filters.append(
                FilterCriteria(
                    entity=self.__class__.__pydantic_generic_metadata__["args"][0],
                    attribute=metadata[0],
                    values=values,
                    option=FilterOption(value=metadata[-2]),
                )
            )
        return filters


class PriorityCriteria(EntityBasedCriteria):
    asc: bool = Field(default=True)

    def to_sql_priority(self) -> Any:
        raise NotImplementedError("Method is not implemented")


class PrioritizeRequest(BaseModel, Generic[T]):
    priorities: str | None = Field(default=None)

    @field_validator("priorities")
    def validate_priorities(cls, v):
        if not v:
            return v
        candidates = v.split(sep=";")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            if len(metadata) > 2:
                raise ValueError(
                    "Invalid priority format. Expected '[attribute] [ASC|DESC]'"
                )
            if not metadata[0]:
                raise ValueError("Attribute is required")
            entity_type = cls.__pydantic_generic_metadata__["args"][0]
            if not hasattr(entity_type, metadata[0]):
                raise ValueError(
                    f"'{metadata[0]}' is not an attribute of {entity_type.__name__}"
                )
            if len(metadata) != 1 and metadata[1] not in {"ASC", "DESC"}:
                raise ValueError("Sorting order must be ASC or DESC")
        return v

    def resolve_priorities(self):
        """Resolves priority string into PriorityCriteria objects.

        Returns:
            list[PriorityCriteria]: List of parsed priority criteria
        """
        if not self.priorities:
            return []
        priorities: list[PriorityCriteria] = []
        candidates = self.priorities.split(sep=";")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            priorities.append(
                PriorityCriteria(
                    entity=self.__class__.__pydantic_generic_metadata__["args"][0],
                    attribute=metadata[0],
                    asc=len(metadata) == 1 or metadata[1] == "ASC",
                )
            )
        return priorities


class QueryRequest(PageRequest, FilterRequest[T], PrioritizeRequest[T], Generic[T]):
    pass
