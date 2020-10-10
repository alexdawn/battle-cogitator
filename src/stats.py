from typing import List, Dict
from math import sqrt, pow


def mean(values: List[float]) -> float:
    return sum(values) / len(values)


def standard_deviation(values: List) -> float:
    mu = mean(values)
    return sqrt(
        1 / (len(values) - 1) * sum(
            pow(x - mu, 2)
            for x in values)
    )


def get_stats(values: List) -> Dict[str, float]:
    values = [x for x in values if x]
    if len(values) > 2:
        return {
            # "min": min(values),
            "mean": mean(values),
            # "max": max(values),
            "std": round(standard_deviation(values), 2)
        }
    else:
        return {}
