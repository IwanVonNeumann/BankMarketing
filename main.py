from random import shuffle

from sklearn.ensemble import RandomForestClassifier

from service import dao
from service.dataset_utils import extract_keys, extract_values
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

k = 20
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

# feature_names = ['prob_eval'] + feature_names
# print(feature_names)
# test_records = [[p] + item for item, p in (problem, success_probabilities)]

for i in range(k):
    print("Client:", dict(zip(feature_names, test_records[i])))
    print('y' if answer[i] == 1 else 'n')
    print("%.2f\n" % success_probabilities[i])

print("Model precision:", rfClassifier.oob_score_)
