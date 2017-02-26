def print_overall_stats(data):
    print("Records total:", len(data))
    positive_rec = [item for item in data if item["y"] == "yes"]
    negative_rec = [item for item in data if item["y"] == "no"]
    print("Positive results:", len(positive_rec))
    print("Negative results:", len(negative_rec))
    print("Positive rate:", len(positive_rec) / len(data))
