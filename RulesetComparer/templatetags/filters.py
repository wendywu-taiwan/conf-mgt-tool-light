from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_map_add_array(dictionary, map_key):
    return get_map_array(dictionary, map_key, 0)


@register.filter
def get_map_remove_array(dictionary, map_key):
    return get_map_array(dictionary, map_key, 1)


@register.filter
def get_map_modify_array(dictionary, map_key):
    return get_map_array(dictionary, map_key, 2)


def get_map_array(dictionary, map_key, index):
    for key in dictionary:
        if key != map_key:
            continue
        else:
            result_list = list(dictionary[key].values())
            return result_list[index]


@register.filter
def get_array_split_by_comma(array):
    if array is None:
        return ""
    return array.split(",")
