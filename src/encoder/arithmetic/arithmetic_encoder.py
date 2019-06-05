import operator
import string
from collections import defaultdict
from decimal import Decimal
from typing import Dict, Tuple, Union


class Range:
    def __init__(self, x: Union[Decimal, int, float] = Decimal(0), y: Union[Decimal, int, float] = Decimal(0)):
        self.x = x if isinstance(x, Decimal) else Decimal(x)
        self.y = y if isinstance(y, Decimal) else Decimal(y)


def _create_probabilities(data: bytes) -> dict:
    """
    obtain P(n) for all 256 bytes

    [ b'\x00' ; b'\xff' ]
    """
    frequencies = dict.fromkeys(range(0, 256), Decimal(0))  # alphabet power (supply)  = 256
    for byte in data:
        frequencies[byte] += 1  # count of each symbol

    length = Decimal(len(data))  # total symbols count
    probabilities = dict(sorted(frequencies.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))  # sort by desc freq
    for byte, count in probabilities.items():
        probabilities[byte] = Decimal(count) / Decimal(length)  # probability of each symbol

    return probabilities


def _create_ranges(probabilities: dict) -> Dict[bytes, Range]:
    left_gap: Decimal = Decimal(0)
    ranges = {}

    for byte, probability in probabilities.items():
        right_gap = left_gap + probability
        ranges[byte] = Range(left_gap, right_gap)
        left_gap = right_gap

    return ranges


def encode(data):
    probabilities = _create_probabilities(data)
    ranges = _create_ranges(probabilities)
    cr = Range(0, 1)
    for byte in data:
        delta = cr.y - cr.x
        cr.y = delta * ranges[byte].y + cr.x  # y fist b'cose x use in y counting
        cr.x = delta * ranges[byte].x + cr.x
    return cr.x


if __name__ == '__main__':
    # a = 0.79052344320
    data = bytes([0, 1, 2, 1, 2, 2, 0, 1, 2, 10])
    coded = encode(data)
    print(coded)
