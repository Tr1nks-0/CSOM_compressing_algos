import operator
import string
from collections import defaultdict
from decimal import Decimal
from typing import Dict, Tuple


def encode(data: bytes) -> bytes:
    pass


def _create_probabilities(data: bytes) -> dict:
    probabilities = dict.fromkeys(range(0, 256), Decimal(0))  # alphabet power (supply)  = 256
    for byte in data:
        probabilities[byte] += 1  # count of each symbol

    length = Decimal(len(data))  # total symbols count
    for byte, count in probabilities.items():
        probabilities[byte] = Decimal(count) / Decimal(length)  # probability of each symbol

    return probabilities


def _create_ranges(probabilities: dict) -> Dict[bytes, Tuple[Decimal, Decimal]]:
    left_gap: Decimal = Decimal(0)
    ranges = {}

    for byte, probability in probabilities.items():
        right_gap = left_gap + probability
        ranges[byte] = (left_gap, right_gap)
        left_gap = right_gap

    return ranges


def encode(data):
    probabilities = _create_probabilities(data)
    ranges = _create_ranges(probabilities)
    left_gap: Decimal = Decimal(0)
    right_gap: Decimal = Decimal(1)
    for byte in data:
        foo = right_gap - left_gap
        right_gap = foo * ranges[byte][1] + left_gap
        left_gap = foo * ranges[byte][0] + left_gap
    return left_gap




if __name__ == 'main':
    data = bytes([0b1, 0b1, 0b10, 0b10, 0b10, 0b11, 0b11, 0b11, 0b11])
    coded = encode(data)
    print(coded)
