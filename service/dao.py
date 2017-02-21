import csv

DATA_PATH = "data/bank.csv"


def get_csv_data(delimiter=',', quotechar='"'):
    stream = open(DATA_PATH, newline='')
    return list(csv.reader(stream, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_NONNUMERIC))


def get_mapped_data(delimiter=',', quotechar='"'):
    rows = get_csv_data(delimiter=delimiter, quotechar=quotechar)
    feature_names = rows[0]
    raw_data = rows[1:]
    mapped_data = [dict(zip(feature_names, item)) for item in raw_data]
    return mapped_data
