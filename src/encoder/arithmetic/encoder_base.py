

# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N2
class ArithmeticCoderBase(object):
    DATA_BITS_COUNT = 32
    MAX_RANGE = 1 << DATA_BITS_COUNT
    RANGE_HALF = MAX_RANGE >> 1
    RANGE_QUARTER = RANGE_HALF >> 1
    MIN_RANGE = RANGE_HALF + 2
    MAX_OPERATOR_LENGTH = MIN_RANGE
    MASK = MAX_RANGE - 1

    def __init__(self, numbits):
        self.CRx = 0
        self.CRy = self.MASK

    def update(self, freqs, symbol):
        CRx = self.CRx
        CRy = self.CRy
        delta = CRy - CRx + 1

        amount = freqs.amount
        symlow = freqs.accumulated_x(symbol)
        symhigh = freqs.accumulated_y(symbol)
        if symlow == symhigh:
            raise ValueError("Symbol has zero frequency")
        if amount > self.MAX_OPERATOR_LENGTH:
            raise ValueError("Cannot code symbol because total is too large")

        newhigh = CRx + symhigh * delta // amount - 1
        newlow = CRx + symlow * delta // amount
        self.CRx = newlow
        self.CRy = newhigh

        while ((self.CRx ^ self.CRy) & self.RANGE_HALF) == 0:
            self.shift()
            self.CRx = ((self.CRx << 1) & self.MASK)
            self.CRy = ((self.CRy << 1) & self.MASK) | 1
        while (self.CRx & ~self.CRy & self.RANGE_QUARTER) != 0:
            self.underflow()
            self.CRx = (self.CRx << 1) ^ self.RANGE_HALF
            self.CRy = ((self.CRy ^ self.RANGE_HALF) << 1) | self.RANGE_HALF | 1

    def shift(self):
        raise NotImplementedError()

    def underflow(self):
        raise NotImplementedError()


class ArithmeticEncoder(ArithmeticCoderBase):

    def __init__(self, numbits, bitout):
        super(ArithmeticEncoder, self).__init__(numbits)
        self.output = bitout
        self.num_underflow = 0

    def write(self, freqs, symbol):
        self.update(freqs, symbol)

    def finish(self):
        self.output.write(1)

    def shift(self):
        bit = self.CRx >> (self.DATA_BITS_COUNT - 1)
        self.output.write(bit)

        for _ in range(self.num_underflow):
            self.output.write(bit ^ 1)
        self.num_underflow = 0

    def underflow(self):
        self.num_underflow += 1


class ArithmeticDecoder(ArithmeticCoderBase):

    def __init__(self, numbits, bitin):
        super(ArithmeticDecoder, self).__init__(numbits)
        self.input = bitin
        self.code = 0
        for _ in range(self.DATA_BITS_COUNT):
            self.code = self.code << 1 | self.read_code_bit()

    def read(self, freqs):
        amount = freqs.amount
        if amount > self.MAX_OPERATOR_LENGTH: raise ValueError("Cannot decode symbol because total is too large")
        delta = self.CRy - self.CRx + 1
        offset = self.code - self.CRx
        value = ((offset + 1) * amount - 1) // delta
        assert value * delta // amount <= offset
        assert 0 <= value < amount

        start = 0
        end = freqs.length
        while end - start > 1:
            middle = (start + end) >> 1
            if freqs.accumulated_x(middle) > value:
                end = middle
            else:
                start = middle
        assert start + 1 == end

        symbol = start
        self.update(freqs, symbol)
        if not (self.CRx <= self.code <= self.CRy):
            raise AssertionError("Code out of range")
        return symbol

    def shift(self):
        self.code = ((self.code << 1) & self.MASK) | self.read_code_bit()

    def underflow(self):
        self.code = (self.code & self.RANGE_HALF) | ((self.code << 1) & (self.MASK >> 1)) | self.read_code_bit()

    def read_code_bit(self):
        temp = self.input.read()
        if temp == -1:
            temp = 0
        return temp

