from random import shuffle


def get_balanced_data(data, key_feature, values):
    # TODO extract values here
    split_data = {}
    for value in values:
        split_data[value] = [item for item in data if item[key_feature] == value]

    for key, value in split_data.items():
        print(key, len(value))

    class_len = min([len(x) for x in split_data.values()])
    balanced_data = []

    for key, value in split_data.items():
        shuffle(value)
        balanced_data += value[:class_len]

    return balanced_data
