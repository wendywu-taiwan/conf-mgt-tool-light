def array_filter(array, filter_keys):
    matched_list = []
    for string in array:
        match = True
        string = string.strip()
        lower_string = string.lower()

        for key in filter_keys:
            key = key.strip()
            lower_key = key.lower()
            if lower_key not in lower_string:
                match = False

        if match:
            matched_list.append(string)
    return matched_list


def string_filter(string, filter_keys):
    string = string.strip()
    lower_string = string.lower()

    match = True
    for key in filter_keys:
        key = key.strip()
        lower_key = key.lower()
        if lower_key not in lower_string:
            match = False
            break

    return match


def folder_filter(country, folder_path, filter_keys):
    folder_path = folder_path.strip()
    folder_path = folder_path.lower()

    for key in filter_keys:
        full_path = "/" + country + key
        full_path = full_path.strip()
        full_path = full_path.lower()
        if folder_path == full_path:
            return True
    return False
