import math
from fractions import Fraction
from typing import Dict, Tuple, Union, BinaryIO

from encoder.arithmetic.range import Range
# REC = 100
from encoder.encoder import Encoder

EOF_KEY = 256


class ArithmeticEncoder(Encoder):
    def __init__(self):
        super().__init__()
        self.default_extension = 'armc'
        self.name = 'Arithmetic'

    def compress_to_io(self, data: bytes, io: BinaryIO) -> tuple:
        data, meta = self.compress_to_bytes(data)
        io.write(data)
        return meta

    def restore_from_io(self, io: BinaryIO) -> bytes:
        # if nodes_count == 0:
        #     return bytes()
        data = io.read()
        return self.restore_from_bytes(data)

    def compress_to_bytes(self, data: bytes) -> Tuple[bytes, tuple]:
        coded = self._calculate_code_range(data)
        code_point = self._calculate_code_point(coded)
        code_point_bytes = self._code_point_to_bytes(code_point)
        return code_point_bytes, self.calculate_meta(len(data), len(code_point_bytes))

    def restore_from_bytes(self, data: bytes) -> bytes:
        code_point = self._bytes_to_code_point(data)
        fraction = self._code_point_to_fraction(code_point)
        decoded = self._restore_from_code_range(fraction)
        return decoded

    def _calculate_code_range(self, data: bytes) -> Range:
        frequencies, ranges, eof = self._create_initial_ranges()
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

    def _restore_from_code_range(self, data: Fraction) -> bytes:
        restored = bytearray()
        frequencies, ranges, _ = self._create_initial_ranges()
        not_end = True
        i = 0
        while not_end:
            byte, range_n = self._get_range_by_decimal(ranges, data)
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

    def _create_ranges(self, frequencies: Dict[int, int], count: Union[int, Fraction]) -> (Dict[int, Range], Range):
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

    def _create_initial_ranges(self) -> Tuple[Dict[int, int], Dict[int, Range], Range]:
        frequencies = dict.fromkeys(range(256), Fraction(1))
        frequencies[EOF_KEY] = Fraction(1)
        ranges, eof = self._create_ranges(frequencies, 257)
        return frequencies, ranges, eof

    def _get_range_by_decimal(self, ranges: Dict[int, Range], num: Fraction):
        for byte, range in ranges.items():
            if range.is_in_range(num):
                return byte, range
        raise RuntimeError('Passed number is out of range of all ranges')

    def _calculate_code_point(self, range: Range, denom=1, n=0) -> (int, int):
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
            return self._calculate_code_point(range, denom * 2, n + 1)

    def _code_point_to_bytes(self, point: Tuple[int, int]) -> bytes:
        numerator_bits = bin(point[0])[2:].zfill(point[1])
        bit_count = len(numerator_bits) + 3
        reduced_bit_count = math.ceil(bit_count / 8) * 8
        byte_complete_offset = reduced_bit_count - bit_count
        bit_str = bin(byte_complete_offset)[2:].zfill(3) + numerator_bits + '0' * byte_complete_offset
        b = bytes(int(bit_str[index:index + 8], 2) for index in range(0, len(bit_str), 8))
        return b

    def _bytes_to_code_point(self, data: bytes) -> (int, int):
        reduced_bit_count = len(data) * 8
        data_int = int.from_bytes(data, 'big')
        data_bits = bin(data_int)[2:].zfill(reduced_bit_count)
        byte_complete_offset = int(data_bits[:3], 2)
        data_bits = data_bits[3:len(data_bits) - byte_complete_offset]
        numerator = int(data_bits, 2)
        n = len(data_bits)
        return numerator, n

    def _code_point_to_fraction(self, code_point: Tuple[int, int]) -> Fraction:
        return Fraction(code_point[0], 1 << code_point[1])
