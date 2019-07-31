def string_builder(str_list):
    return "".join(str_list)


def get_union(list_a, list_b):
    return [i for i in list_a if i in list_b]


def to_int_list(my_list):
    return [int(i) for i in my_list]


def contains(my_list, text):
    if str(text) in str(my_list):
        return True
    else:
        return False
