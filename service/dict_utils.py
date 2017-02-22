def replace_value(item, field_name, dictionary, default_value='OTHER'):
    if item[field_name] not in dictionary:
        item[field_name] = default_value
    return item


def format_dict(d, precision):
    return {k: round(v, precision) if isinstance(v, float) else v for k, v in d.items()}
