from service import dao

data = dao.get_csv_data(delimiter=";")

feature_names = data[0]
values = data[1:]

print("Records total:", len(values))
print("Feature names:")
print(feature_names)
