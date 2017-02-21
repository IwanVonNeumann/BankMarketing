def replace_value(item, field_name, dictionary, default_value='OTHER'):
    if item[field_name] not in dictionary:
        item[field_name] = default_value
    return item
