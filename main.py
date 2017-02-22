from service import dao
from service.preprocessing import pre_process
from service.stats import print_overall_stats

data = dao.get_mapped_data(delimiter=";")

binary_fields = ['default', 'housing', 'loan', 'y']

FREQUENCY_THRESHOLD = 0.05
categorical_fields = [
    {'name': 'job', 'frequency_threshold': FREQUENCY_THRESHOLD},
    {'name': 'marital', 'frequency_threshold': FREQUENCY_THRESHOLD},
    {'name': 'education', 'frequency_threshold': FREQUENCY_THRESHOLD},
    {'name': 'contact', 'frequency_threshold': FREQUENCY_THRESHOLD},
    {'name': 'month', 'frequency_threshold': FREQUENCY_THRESHOLD},
    {'name': 'poutcome', 'frequency_threshold': 0}
]

print_overall_stats(data)

for i in range(0, 5):
    print(data[i])

pre_process(data, binary_fields, categorical_fields)

print("------------------")

for i in range(0, 5):
    print(data[i])
