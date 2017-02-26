from service.dataset_utils import process_all_binary_fields, process_all_categorical_fields, filter_data, \
    remove_fields_from_dataset


def pre_process(data, records_to_remove, fields_to_remove, binary_fields, categorical_fields, default_value='OTHER',
                verbose=False):
    filtered_data = filter_data(data, records_to_remove, verbose=verbose)
    remove_fields_from_dataset(data, fields_to_remove, verbose=verbose)
    process_all_binary_fields(filtered_data, binary_fields)
    process_all_categorical_fields(filtered_data, categorical_fields, default_value=default_value, verbose=verbose)
    return filtered_data
