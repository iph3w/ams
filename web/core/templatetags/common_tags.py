import json
import typing
from django import template

register = template.Library()


@register.filter
def get_dict_value(dictionary: dict, key: str) -> typing.Any:
    if key in dictionary.keys():
        return dictionary[key]
    return ''


@register.filter
def get_str_dict_value(dictionary: str, key: str) -> typing.Any:
    if dictionary is None or dictionary == '':
        return ''
    _dictionary = json.loads(dictionary)
    if key in _dictionary.keys():
        return _dictionary[key]
    return ''


@register.filter
def str_to_dict(dictionary: str) -> dict:
    if dictionary is None or dictionary == '':
        return ''
    return json.loads(dictionary)


@register.filter
def dict_items(dictionary: dict) -> typing.Any:
    return dictionary.items()


@register.filter
def str_to_dict_items(dictionary: str) -> dict:
    if dictionary is None or dictionary == '':
        return {}
    return json.loads(dictionary).items()
