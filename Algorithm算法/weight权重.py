import bisect
import random
from collections import namedtuple

weight = namedtuple("weight", ["power"])

A_weight = weight(50)
B_weight = weight(30)
C_weight = weight(70)

compare_weight = [A_weight, B_weight, C_weight]


def check_power(weights):
    """计算总和"""
    power_count = sum(_weight.power for _weight in weights)
    """权重区间"""
    power_list = list(get_power_list(weights))
    """随机权重"""
    random_power = random.uniform(0, power_count)
    """权重落点"""
    fit = weights[bisect.bisect(power_list, random_power)]
    return fit


def get_power_list(weights):
    current_power = 0
    for weight in weights:
        current_power += weight.power
        yield current_power


_fit = check_power(compare_weight)

print(_fit)
