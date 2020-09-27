from typing import List, Dict
from math import sqrt, pow


def mean(values: List[float]) -> float:
    try:
        return sum(values) / len(values)
    except:
        import pdb
        pdb.set_trace()


def standard_deviation(values: List[float]) -> float:
    mu = mean(values)
    return sqrt(
        1 / (len(values) - 1)
        * sum(
            pow(x - mu, 2)
            for x in values)
    )


def get_stats(values: List[float]) -> Dict[str, float]:
    if len(values) > 0:
        return {
            "mean": mean(values),
            "std": round(standard_deviation(values), 2)
        }
    else:
        return "No value"
