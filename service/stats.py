
def print_overall_stats(data):
    print("Records total:", len(data))
    positive_rec = len([item for item in data if item["y"] == "yes"])
    negative_rec = len([item for item in data if item["y"] == "no"])
    print("Positive results:", positive_rec)
    print("Negative results:", negative_rec)
