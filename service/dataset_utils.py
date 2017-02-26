from sklearn.feature_extraction import DictVectorizer

from service.dict_utils import replace_value, format_dict
from service.list_utils import get_merged_rare_values_dict
from service.logger import log

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


def pack_all_categorical_fields(data, categorical_fields, default_value='OTHER', verbose=False):
    log("Categorical fields' stats:", verbose=verbose)
    for field in categorical_fields:
        values = [item[field['name']] for item in data]
        log(field['name'], verbose=verbose)
        merged_values = get_merged_rare_values_dict(values, field['frequency_threshold'], verbose=verbose)
        log(format_dict(merged_values, 3), verbose=verbose)
        for item in data:
            replace_value(item, field['name'], merged_values, default_value=default_value)


def map_feature_names_to_data(headers, data):
    return [dict(zip(headers, item)) for item in data]


def split_all_categorical_fields(data, key_feature='y', verbose=False):
    dict_vectorizer = DictVectorizer()

    transformed_data = list(dict_vectorizer.fit_transform(data).toarray())
    feature_names = dict_vectorizer.get_feature_names()

    if verbose:
        print("Features before:", len(data[0]))
        print("Features after:", len(feature_names))
        print(feature_names)

    return map_feature_names_to_data(feature_names, transformed_data)


def remove_field(item, field_name):
    del item[field_name]


def remove_field_from_dataset(data, field_name, verbose=False):
    log("Removing field from all records:", field_name, verbose=verbose)
    for item in data:
        remove_field(item, field_name)


def remove_fields_from_dataset(data, field_names, verbose=False):
    for field_name in field_names:
        remove_field_from_dataset(data, field_name, verbose=verbose)


def filter_data(data, rules, verbose=False):
    filtered_data = data
    log("Filtering dataset...", verbose=verbose)
    for rule in rules:
        filtered_data = filter(lambda item: item[rule['name']] != rule['value'], filtered_data)
    result = list(filtered_data)
    log("Records dropped:", len(data) - len(result), verbose=verbose)
    return result


def extract_keys(data):
    return list(data[0].keys())


def extract_values(data):
    return [list(item.values()) for item in data]
