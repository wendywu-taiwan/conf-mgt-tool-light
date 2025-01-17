from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_map_add_array(dictionary, map_key):
    return get_map_array(dictionary, map_key, 'add')


@register.filter
def get_map_remove_array(dictionary, map_key):
    return get_map_array(dictionary, map_key, 'remove')


@register.filter
def get_map_modify_array(dictionary, map_key):
    return get_map_array(dictionary, map_key, 'modify')


def get_map_array(dictionary, map_key, dict_key):
    for key in dictionary:
        if key != map_key:
            continue
        else:
            result_list = dictionary[key].get(dict_key)
            return result_list


@register.filter
def get_array_split_by_comma(array):
    if array is None:
        return ""
    return array.split(",")


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def add(value, arg):
    return value + arg


@register.filter
def add_str(arg1, arg2):
    return str(arg1) + str(arg2)


@register.filter()
def parse_space(value):
    return mark_safe("&ensp;".join(value.split(' ')))


@register.filter()
def parse_space_large(value):
    return mark_safe("&ensp;&ensp;".join(value.split('  ')))


@register.filter()
def parse_tab(value):
    return mark_safe("&ensp;&ensp;&ensp;&ensp;".join(value.split('\t')))
