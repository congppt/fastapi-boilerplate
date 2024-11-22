import json
from typing import Type, Any, get_args, get_origin, Union

from pydantic import BaseModel

from utils import PRIMITIVES, SUPPORTED_COLLECTIONS
from utils.parser import parse


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj) -> Any:
        if isinstance(obj, BaseModel):
            return obj.model_dump()
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

        origin_type = get_origin(model)
        # handle case when model is primitive/custom
        if origin_type is None:
            if model in PRIMITIVES:
                return model(value)
            else:
                return model(**value)
        return parse(value=value, model=model, hook=json_parse)
    except json.JSONDecodeError:
        # fallback to current value
        return json_str
    except Exception as e:
        # logging
        raise e

def json_parse(value_: Any, model_: Type[Any]) -> Any:
    return json_deserialize(json_serialize(value_), model_)
