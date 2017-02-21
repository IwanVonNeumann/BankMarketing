from service import dao

data = dao.get_mapped_data(delimiter=";")

print("Records total:", len(data))
