from collections import defaultdict
from decimal import Decimal
from typing import Dict, Tuple, Union

from encoder.arithmetic.range import Range

EOF_KEY = 256


def _create_ranges(frequencies: Dict[int, int], count: Union[int, Decimal]) -> (Dict[int, Range], Range):
    left_gap: Decimal = Decimal(0)
    ranges = {}
    if not isinstance(count, Decimal):
        count = Decimal(count)
    for byte, frequency in frequencies.items():
        probability = frequency / count
        right_gap = left_gap + probability
        ranges[byte] = Range(left_gap, right_gap, byte == EOF_KEY)
        left_gap = right_gap

    return ranges, ranges[EOF_KEY]


def _create_initial_ranges() -> Tuple[Dict[int, int], Dict[int, Range], Range]:
    frequencies = dict.fromkeys(range(256), Decimal(1))
    frequencies[EOF_KEY] = Decimal(1)
    ranges, eof = _create_ranges(frequencies, 257)
    return frequencies, ranges, eof


def get_range_by_decimal(ranges: Dict[int, Range], num: Decimal):
    for byte, range in ranges.items():
        if range.is_in_range(num):
            return byte, range
    raise RuntimeError('Passed number is out of range of all ranges')


def encode(data: bytes) -> Decimal:
    frequencies, ranges, eof = _create_initial_ranges()
    cr = Range(0, 1)
    for byte in data:
        frequencies[byte] += 1
        delta = cr.y - cr.x
        cr.y = delta * ranges[byte].y + cr.x  # y fist b'cose x use in y counting
        cr.x = delta * ranges[byte].x + cr.x

    delta = cr.y - cr.x
    cr.x = delta * eof.x + cr.x

    return cr.x


def decode(data: Decimal) -> bytes:
    restored = bytearray()
    frequencies, ranges, _ = _create_initial_ranges()
    not_end = True
    while not_end:
        byte, range_n = get_range_by_decimal(ranges, data)
        if range_n.EOF:
            not_end = False
        else:
            restored.append(byte)
            data = (data - range_n.x) / (range_n.y - range_n.x)

    return bytes(restored)


if __name__ == '__main__':
    data = bytes([0, 1, 2, 1, 2, 2, 0, 1, 2, 3])
    coded = encode(data)
    print(coded)
    decoded = decode(coded, 10)
    print(data)
    print(decoded)
    print(data == decoded)
