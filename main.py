from random import shuffle

from sklearn.ensemble import RandomForestClassifier

from service import dao
from service.dataset_utils import extract_keys, extract_values, map_feature_names_to_data
from service.demo_utils import get_balanced_data
from service.logger import print_delimiter
from service.preprocessing import pre_process
from service.stats import print_overall_stats

data = dao.get_mapped_data(delimiter=";")

binary_fields = ['default', 'housing', 'loan', 'y']

FREQUENCY_THRESHOLD = 0.05
categorical_fields = [
    {'name': 'job', 'frequency_threshold': FREQUENCY_THRESHOLD},
    {'name': 'marital', 'frequency_threshold': FREQUENCY_THRESHOLD},
    {'name': 'education', 'frequency_threshold': FREQUENCY_THRESHOLD},
    # {'name': 'contact', 'frequency_threshold': FREQUENCY_THRESHOLD},
    {'name': 'month', 'frequency_threshold': FREQUENCY_THRESHOLD},
    # {'name': 'poutcome', 'frequency_threshold': 0}
]

data = get_balanced_data(data, 'y', ['yes', 'no'])

print_overall_stats(data)

print_delimiter()

records_to_remove = [
    {'name': 'job', 'value': 'unknown'},
    {'name': 'education', 'value': 'unknown'}
]

fields_to_remove = ['contact', 'poutcome']

pre_processed_data = pre_process(data, records_to_remove, fields_to_remove, binary_fields, categorical_fields,
                                 verbose=True)
shuffle(pre_processed_data)

print_delimiter()

feature_names = extract_keys(pre_processed_data)
only_values = extract_values(pre_processed_data)

k = 578
n = len(pre_processed_data)

known = only_values[:n - k]
test_records = only_values[-k:]

problem = [x[:-1] for x in test_records]
answer = [x[-1] for x in test_records]

target = [x[-1] for x in known]
train = [x[:-1] for x in known]

rfClassifier = RandomForestClassifier(n_estimators=50, oob_score=True)
rfClassifier.fit(train, target)

class_probabilities = rfClassifier.predict_proba(problem)
success_probabilities = [x[1] for x in class_probabilities]

PROB_EVAL = 'prob_eval'

feature_names = [PROB_EVAL, 'y'] + feature_names
for i in range(0, len(test_records)):
    test_records[i] = [round(success_probabilities[i], 2), answer[i]] + test_records[i]

clients = map_feature_names_to_data(feature_names, test_records)
prioritized_clients = sorted(clients, key=lambda x: x[PROB_EVAL], reverse=True)

# for i in range(k):
#     print("Client:", prioritized_clients[i])
#     print('YES' if prioritized_clients[i]['y'] == 1 else 'NO')
#     print("%.2f\n" % prioritized_clients[i][PROB_EVAL])

print("Model precision:", rfClassifier.oob_score_)

successful_clients_in_test = sum(answer)

print("Total clients in test:", k)
print("Successful clients in test:", successful_clients_in_test)

s = 0
for i in range(k):
    s += prioritized_clients[i]['y']
    print("{0}\t{1:.2f}\t{2:.2f}".format(i + 1, (i + 1) / k * 100, s / successful_clients_in_test * 100))
