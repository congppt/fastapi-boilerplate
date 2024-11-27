import json
from typing import Type, Any

from pydantic import BaseModel

from utils.parser import parse

try:
    from sqlalchemy.engine.row import BaseRow
except ImportError:
    BaseRow = None


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj) -> Any:
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        if isinstance(obj, BaseRow):
            return dict(obj)
        return super().default(obj)


def json_serialize(obj: Any) -> str:
    """
    Serialize an oject into json string
    :param obj: object to serialize"""
    return json.dumps(obj, cls=CustomJSONEncoder)


def json_deserialize(json_str: str, model: Type[Any] = None) -> Any:
    """
    Deserialize a json string into object of given type
    :param json_str: json represented as string
    :param model: model to deserialize
    :return: deserialized object
    """
    try:
        value = json.loads(json_str)
        # return dict/primitive if model not defined
        if model is None:
            return value
        return parse(value=value, model=model, hook=json_parse)
    except json.JSONDecodeError:
        # fallback to current value
        return json_str


def json_parse(value: Any, model: Type[Any]) -> Any:
    return json_deserialize(json_str=json_serialize(value), model=model)
