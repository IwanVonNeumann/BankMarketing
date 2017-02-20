import csv

DATA_PATH = "data/bank.csv"


def get_csv_data(delimiter=',', quotechar='"'):
    stream = open(DATA_PATH, newline='')
    return list(csv.reader(stream, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_NONNUMERIC))
