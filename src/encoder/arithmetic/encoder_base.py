# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N2
from encoder.arithmetic.frequency_table import FrequencyTable
from util.stream.in_stream import BitInputStream
from util.stream.out_stream import BitOutputStream


# промежуток с дельтой границ
class Range:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def delta(self, round=True):
        return self.y - self.x + (1 if round else 0)


# базовые операции сжатия / восстановления
class ArithmeticCoderBase(object):
    DATA_BITS_COUNT = 32  # длинна данных
    MAX_RANGE = 1 << DATA_BITS_COUNT  # максимальное значение
    RANGE_HALF = MAX_RANGE >> 1  # половина промежутка
    RANGE_QUARTER = RANGE_HALF >> 1  # четверть промежутка
    MIN_RANGE = RANGE_QUARTER + 2  # минимальное значение
    MAX_OPERATOR_LENGTH = MIN_RANGE  # максимальная длинна операторов
    MASK = MAX_RANGE - 1  # битовая маска данных

    def __init__(self):

        self.cr = Range(0, self.MASK)  # начальный промежуток 0 - 1

    def round(self, frequencies: FrequencyTable, char):
        self._check_cr()
        self._check_char(char, frequencies)
        amount = frequencies.amount  # сумма всех частот
        self._check_amount(amount)
        delta = self.cr.delta()  # длинна промежутка
        self.cr.y = self.cr.x + frequencies.accumulated_y(char) * delta // amount - 1  # пересчитываем промежуток правая граница
        self.cr.x = self.cr.x + frequencies.accumulated_x(char) * delta // amount  # пересчитываем промежуток левая граница

        while ((self.cr.x ^ self.cr.y) & self.RANGE_HALF) == 0:  # если у границ есть равные биты слева
            self.shift()  # сдвигаем границы вправо, записывая левые биты
            self.cr.x = ((self.cr.x << 1) & self.MASK)
            self.cr.y = ((self.cr.y << 1) & self.MASK) | 1

        while (self.cr.x & ~self.cr.y & self.RANGE_QUARTER) != 0:  # если есть инверсные
            self.underflow()  # то устраняем записью инверсных бит
            self.cr.x = (self.cr.x << 1) ^ self.RANGE_HALF
            self.cr.y = ((self.cr.y ^ self.RANGE_HALF) << 1) | self.RANGE_HALF | 1

    def _check_char(self, char, frequencies):
        if frequencies.accumulated_x(char) == frequencies.accumulated_y(char):
            raise ValueError("Symbol has zero frequency")

    def _check_amount(self, amount):
        if amount > self.MAX_OPERATOR_LENGTH:
            raise ValueError("Cannot code symbol because total is too large")

    def _check_cr(self):
        if self.cr.x >= self.cr.y or (self.cr.x & self.MASK) != self.cr.x or (self.cr.y & self.MASK) != self.cr.y:
            raise AssertionError("CRx or CRy out of range")
        if not (self.MIN_RANGE <= self.cr.delta() <= self.MAX_RANGE):
            raise AssertionError("Range out of range")

    def shift(self):
        raise NotImplementedError()

    def underflow(self):
        raise NotImplementedError()


# реализация сжатия
class ArithmeticEncoder(ArithmeticCoderBase):

    def __init__(self, output: BitOutputStream):
        super(ArithmeticEncoder, self).__init__()
        self.output = output
        self.underflowed = 0

    # пишет байт данных в промежуток
    def write(self, freqs, symbol):
        self.round(freqs, symbol)

    # заканчивает сжатие дописывая бит
    def finalize(self):
        self.output.write(1)
        self.output.flush()

    # сдвинуть промежутки с записью лидирующих бит
    def shift(self):
        bit = self.cr.x >> (self.DATA_BITS_COUNT - 1)
        self.output.write(bit)

        for _ in range(self.underflowed):
            self.output.write(bit ^ 1)
        self.underflowed = 0

    # устанение избыточности
    def underflow(self):
        self.underflowed += 1


# реализация восстановления
class ArithmeticDecoder(ArithmeticCoderBase):

    def __init__(self, input: BitInputStream):
        super().__init__()
        self.input = input
        self.code = 0
        for _ in range(self.DATA_BITS_COUNT):
            self.code = self.code << 1 | self.read_code_bit()

    # прочитать символ из промежутка
    def read(self, freqs: FrequencyTable):
        amount = freqs.amount  # сумма частот
        self._check_amount(amount)
        delta = self.cr.delta()  # длинна кодового промежутка
        offset = self.code - self.cr.x  # смещение кода относительно начала промежутка
        value = ((offset + 1) * amount - 1) // delta  # значение частоты симводла
        self._check_value(amount, delta, offset, value)

        x = 0
        y = freqs.length
        while y - x > 1:
            middle = (x + y) >> 1  # центер промежутка
            if freqs.accumulated_x(middle) > value:  # если слева
                y = middle  # сужаем справа
            else:  # иначе
                x = middle  # сужаем слева
        self._check_range(x, y)
        self._check_offset(amount, x, delta, freqs, offset)
        self.round(freqs, x)
        self._check_code()
        return x

    # сдвинуть промежутки с записью лидирующих бит
    def shift(self):
        self.code = ((self.code << 1) & self.MASK) | self.read_code_bit()

    # восстановление из избыточности
    def underflow(self):
        self.code = (self.code & self.RANGE_HALF) | ((self.code << 1) & (self.MASK >> 1)) | self.read_code_bit()

    # прочитать бит из кода
    def read_code_bit(self):
        temp = self.input.read()
        if temp == -1:
            temp = 0
        return temp

    def _check_code(self):
        if not (self.cr.x <= self.code <= self.cr.y):
            raise AssertionError("Code out of range")

    def _check_offset(self, amount, char, code_point, freqs, offset):
        if not (freqs.accumulated_x(char) * code_point // amount
                <= offset <
                freqs.accumulated_y(char) * code_point // amount):
            raise ValueError('Wrong offset')

    def _check_range(self, x, y):
        if x + 1 != y:
            raise ValueError('Range wrong')

    def _check_value(self, amount, code_point, offset, value):
        if value * code_point // amount > offset or not (0 <= value < amount):
            raise ValueError('Wrong value')
