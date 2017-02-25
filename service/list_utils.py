from collections import Counter

from service.dict_utils import format_dict
from service.logger import log


def count_absolute_frequencies(values):
    return dict(Counter(values))


def count_relative_frequencies(values):
    abs_f = count_absolute_frequencies(values)
    f_sum = sum(abs_f.values())
    return {key: value / f_sum for key, value in abs_f.items()}


def get_merged_rare_values_dict(values, threshold, default_key='OTHER', verbose=False):
    rel_f = count_relative_frequencies(values)

    log(format_dict(rel_f, 3), verbose=verbose)

    major_elements = {key: value for key, value in rel_f.items() if value >= threshold}

    nothing_excluded = len(major_elements) == len(rel_f)
    only_one_value_excluded = len(major_elements) == len(rel_f) - 1
    if nothing_excluded or only_one_value_excluded:
        return rel_f

    minor_f_sum = sum(value for value in rel_f.values() if value < threshold)
    major_elements[default_key] = minor_f_sum
    return major_elements
