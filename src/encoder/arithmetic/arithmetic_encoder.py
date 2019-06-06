from collections import defaultdict
from decimal import Decimal
from typing import Dict

from encoder.arithmetic.range import Range


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


def _create_ranges(probabilities: dict) -> Dict[int, Range]:
    """
    create ranges from probabilities. Total summ of probabilities should be equal 1
    """
    left_gap: Decimal = Decimal(0)
    ranges = {}

    for byte, probability in probabilities.items():
        right_gap = left_gap + probability
        ranges[byte] = Range(left_gap, right_gap)
        left_gap = right_gap

    return ranges


def _create_initial_ranges() -> Dict[int, Range]:
    ranges = {}
    probability = Decimal(1) / Decimal(257)
    left_gap: Decimal = Decimal(0)
    right_gap: Decimal = Decimal(0)
    for byte in range(0, 256):
        right_gap = left_gap + probability
        ranges[byte] = Range(left_gap, right_gap)
        left_gap = right_gap
    ranges[257] = Range(left_gap, right_gap, EOF=True)
    return ranges


def encode(data: bytes) -> Decimal:
    ranges = _create_initial_ranges()
    frequencies = defaultdict(int)
    cr = Range(0, 1)
    for byte in data:
        frequencies[byte] += 1
        delta = cr.y - cr.x
        cr.y = delta * ranges[byte].y + cr.x  # y fist b'cose x use in y counting
        cr.x = delta * ranges[byte].x + cr.x

    return cr.x, ranges


def get_range_by_decimal(ranges: Dict[int, Range], num: Decimal):
    for byte, range in ranges.items():
        if range.is_in_range(num):
            return byte, range
    raise RuntimeError('Passed number is out of range of all ranges')


def decode(data: Decimal, length: int) -> bytes:
    restored = bytearray()
    ranges = _create_initial_ranges()
    for i in range(length):
        byte, range_n = get_range_by_decimal(ranges, data)
        restored.append(byte)
        data = (data - range_n.x) / (range_n.y - range_n.x)

    return bytes(restored)


if __name__ == '__main__':
    # a = 0.79052344320
    data = bytes([0, 1, 2, 1, 2, 2, 0, 1, 2, 10])
    coded, ranges = encode(data)
    print(coded)
    decoded = decode(coded, 10, ranges)
    print(data)
    print(decoded)
    print(data == decoded)
