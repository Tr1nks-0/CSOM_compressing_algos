import math
from decimal import Decimal
from fractions import Fraction
from typing import Dict, Tuple, Union

from encoder.arithmetic.range import Range

# REC = 100

EOF_KEY = 256


def encode(data: bytes) -> Range:
    frequencies, ranges, eof = _create_initial_ranges()
    cr = Range(0, 1)
    i = 0
    for byte in data:
        # if i >= REC:
        #     print('rec')
        #     ranges, eof = _create_ranges(frequencies, 257)
        #     i = 0
        # i += 1
        frequencies[byte] += 1
        delta = cr.y - cr.x
        cr.y = delta * ranges[byte].y + cr.x  # y fist b'cose x use in y counting
        cr.x = delta * ranges[byte].x + cr.x
        # print(f'{byte} - [ {cr.x} ; {cr.y} ]')

    delta = cr.y - cr.x
    cr.y = delta * eof.y + cr.x
    cr.x = delta * eof.x + cr.x

    return cr


def decode(data: Fraction) -> bytes:
    restored = bytearray()
    frequencies, ranges, _ = _create_initial_ranges()
    not_end = True
    i = 0
    while not_end:
        byte, range_n = _get_range_by_decimal(ranges, data)
        # print(f'{byte} - [ {range_n.x} ; {range_n.y} ]')
        # if i >= REC:
        #     print('rec')
        #     ranges, _ = _create_ranges(frequencies, 257)
        #     i = 0
        # i += 1
        frequencies[byte] += 1
        if range_n.EOF:
            not_end = False
        else:
            restored.append(byte)
            data = (data - range_n.x) / (range_n.y - range_n.x)

    return bytes(restored)


def _create_ranges(frequencies: Dict[int, int], count: Union[int, Fraction]) -> (Dict[int, Range], Range):
    left_gap: Fraction = Fraction(0)
    ranges = {}
    if not isinstance(count, Fraction):
        count = Fraction(count)
    for byte, frequency in frequencies.items():
        probability = frequency / count
        right_gap = left_gap + probability
        ranges[byte] = Range(left_gap, right_gap, byte == EOF_KEY)
        left_gap = right_gap

    return ranges, ranges[EOF_KEY]


def _create_initial_ranges() -> Tuple[Dict[int, int], Dict[int, Range], Range]:
    frequencies = dict.fromkeys(range(256), Fraction(1))
    frequencies[EOF_KEY] = Fraction(1)
    ranges, eof = _create_ranges(frequencies, 257)
    return frequencies, ranges, eof


def _get_range_by_decimal(ranges: Dict[int, Range], num: Fraction):
    for byte, range in ranges.items():
        if range.is_in_range(num):
            return byte, range
    raise RuntimeError('Passed number is out of range of all ranges')


def _calculate_code_point(range: Range, denom=1, n=0) -> (int, int):
    while denom < range.x.denominator:
        n += 1
        denom = denom << 1

    num_tmp = range.x.numerator * denom
    if num_tmp % range.x.denominator:
        num = num_tmp // range.x.denominator + 1  # use int division and add 1 for rounding up to avoid float overflow
    else:
        num = num_tmp // range.x.denominator  # use int division to avoid float overflow

    if range.x <= Fraction(num, denom) < range.y:
        return num, n
    else:
        return _calculate_code_point(range, denom * 2, n + 1)


def _code_point_to_bytes(point: Tuple[int, int]) -> bytes:
    num_bits = bin(point[0])[2:]

    return bytes(1)


if __name__ == '__main__':
    data = bytes([0, 1, 2, 1, 2, 2, 0, 1, 2, 3])
    coded = encode(data)
    code_point = _calculate_code_point(coded)
    print(code_point)
    cpb = _code_point_to_bytes(code_point)
    print('-----------------')
    decoded = decode(Fraction(code_point[0], 1 << code_point[1]))
    print(data)
    print(decoded)
    print(data == decoded)
