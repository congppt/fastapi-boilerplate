import json
from typing import Type, Any, get_args, get_origin, Union

from pydantic import BaseModel


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj) -> Any:
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)

def json_serialize(obj: Any) -> str:
    """Serialize an oject into json string"""
    return json.dumps(obj, cls=CustomJSONEncoder)

__SUPPORTED_COLLECTIONS = (list, set, tuple)
__PRIMITIVES = (int, str, bytes, float, bool, complex)

def __union_deserialize(value: Any, union_types: tuple) -> Any:
    """Deserialize value to given type union"""
    for typ in union_types:
        try:
            if typ in __PRIMITIVES:
                return typ(value)
            return json_deserialize(json_serialize(value), typ)
        except (ValueError, TypeError):
            continue
    raise TypeError(f"{json_serialize(value)} cannot be deserialized into any type in {union_types}")

def json_deserialize(json_str: str, model: Type[Any] = None) -> Any:
    """Deserialize a json string into object of given type"""
    try:
        value = json.loads(json_str)
        # return dict/primitive if model not defined
        if model is None:
            return value

        origin_type = get_origin(model)
        # handle case when model is primitive/custom
        if origin_type is None:
            if model in __PRIMITIVES:
                return model(value)
            else:
                return model(**value)

        # handle case when model is collection
        if origin_type in __SUPPORTED_COLLECTIONS:
            if not isinstance(value, list):
                raise TypeError(f"{json_serialize(value)} is not of collection type.")
            element_types = get_args(model)
            # handle case when model element type is not fixed to only 1 type
            if element_types and get_origin(element_types[0]) is Union:
                union_types = get_args(element_types[0])
                deserialized_values = [__union_deserialize(val, union_types) for val in value]
            # handle case when model element type is not defined/one type only
            else:
                element_type = element_types[0] if element_types else None
                if element_type in __PRIMITIVES:
                    deserialized_values = [element_type(val) for val in value]
                else:
                    deserialized_values = [json_deserialize(json_serialize(val), element_type) for val in value]
            return model(deserialized_values)

        raise TypeError(f"{model.__name__} is not supported yet.")
    except json.JSONDecodeError:
        # fallback to current value
        return json_str
    except Exception as e:
        raise e
