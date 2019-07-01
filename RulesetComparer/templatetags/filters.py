from django import template

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
