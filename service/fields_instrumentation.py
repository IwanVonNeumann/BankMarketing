from service.dict_utils import replace_value
from service.list_utils import get_merged_rare_values_dict

BINARY_DICT = {'no': 0, 'yes': 1}


def substitute_values(item, field_name, dictionary):
    value = item[field_name]
    item[field_name] = dictionary[value]
    return item


def process_binary_field(item, field_name):
    substitute_values(item, field_name, BINARY_DICT)


def process_all_binary_fields(data, field_names):
    for item in data:
        for field_name in field_names:
            process_binary_field(item, field_name)


def process_all_categorical_fields(data, categorical_fields, default_value='OTHER'):
    for field in categorical_fields:
        values = [item[field["name"]] for item in data]
        merged_values = get_merged_rare_values_dict(values, field["frequency_threshold"])
        # print(field["name"], {k: round(v, 3) if isinstance(v, float) else v for k, v in merged_values.items()})
        for item in data:
            replace_value(item, field["name"], merged_values, default_value=default_value)
