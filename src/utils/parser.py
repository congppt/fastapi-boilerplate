from typing import Any, Type, get_origin, get_args, Union, Callable

from utils import PRIMITIVES, SUPPORTED_COLLECTIONS


def union_parse(value: Any, types: tuple, hook: Callable[[Any, Type[Any]], Any]) -> Any:
    """
    Parse value to one of given types that matched
    :param value: value to convert
    :param types: types
    :param hook: custom handler for non-primitive types
    """
    for typ in types:
        try:
            if typ in PRIMITIVES:
                return typ(value)
            return hook(value, typ)
        except (ValueError, TypeError):
            continue
    raise TypeError(f"{value} cannot be deserialized into any type in {types}")


def parse(value: Any, model: Type[Any], hook: Callable[[Any, Type[Any]], Any]) -> Any:
    """
    Parse value into object of given type
    :param value: original value
    :param model: target model
    :param hook: custom handler for non-primitive types
    :return: parsed object
    """
    origin_type = get_origin(model)
    # handle case when model is primitive/custom
    if origin_type is None:
        if model in PRIMITIVES:
            return model(value)
        else:
            return model(**value)
    if origin_type is dict:
        return dict(value)
    # handle case when model is collection
    if origin_type in SUPPORTED_COLLECTIONS:
        if not isinstance(value, list):
            raise TypeError(f'{value} is not a collection')
        element_types = get_args(model)
        # handle case when model element type is not fixed to only 1 type
        if element_types and get_origin(element_types[0]) is Union:
            union_types = get_args(element_types[0])
            parsed_values = [union_parse(val, union_types, hook) for val in value]
        # handle case when model element type is not defined/one type only
        else:
            element_type = element_types[0] if element_types else None
            if element_type in PRIMITIVES:
                parsed_values = [element_type(val) for val in value]
            else:
                parsed_values = [hook(val, element_type) for val in value]
        return model(parsed_values)

    raise TypeError(f"{model.__name__} is not supported yet.")
