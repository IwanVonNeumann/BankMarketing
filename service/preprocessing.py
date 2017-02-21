from service.fields_instrumentation import process_all_binary_fields, process_all_categorical_fields


def pre_process(data, binary_fields, categorical_fields, default_value='OTHER'):
    process_all_binary_fields(data, binary_fields)
    process_all_categorical_fields(data, categorical_fields, default_value=default_value)
