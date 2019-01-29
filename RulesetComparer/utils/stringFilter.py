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
