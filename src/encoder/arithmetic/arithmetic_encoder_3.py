# ALPHABET_SIZE = 258  # use 258 because it more dividable
ALPHABET_SIZE = 6  # use 258 because it more dividable
# EOF = 256
EOF = 5
# OPERATORS_SIZE = 8
OPERATORS_SIZE = 4


class Range:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def delta(self):
        return self.y - self.x + 1

    def str(self):
        return Range(str(self.x), str(self.y))


def create_initial_ranges() -> list:
    ranges = []
    probability = 1 / 258
    for i in range(ALPHABET_SIZE):
        x = ranges[i - 1].y if i > 0 else 0
        y = x + probability
        ranges.insert(i, Range(x, y))
    return ranges


def initialize():
    # ranges = create_initial_ranges()
    ranges = [
        Range(0.5, 1),  # S
        Range(0.4, 0.5),  # W
        Range(0.2, 0.4),  # I
        Range(0.1, 0.2),  # M
        Range(0, 0.1),  # _
    ]
    cr = Range(int('0' * OPERATORS_SIZE), int('9' * OPERATORS_SIZE))
    return ranges, cr, cr.delta()


def recalculate_cr(cr: Range, r: Range):
    delta = cr.delta()
    cr.y = int(cr.x + delta * r.y)-1
    cr.x = int(cr.x + delta * r.x)
    return cr


def shift_cr(cr, crs):
    cr.x = int(crs.x[1:] + '0')
    cr.y = int(crs.y[1:] + '9')
    return cr


def encode(raw_data: bytes):
    ranges, cr, delta = initialize()
    answer = 0
    for char in raw_data:
        range = ranges[char]
        cr = recalculate_cr(cr, range)
        crs = cr.str()
        if crs.x[0] == crs.y[0]:
            answer = answer * 10 + int(crs.x[0])
            cr = shift_cr(cr, crs)

    # range = ranges[EOF]
    # cr = recalculate_cr(cr, range)
    crs = cr.str()
    answer = answer * 10 ** len(crs.x) + int(crs.x)
    return answer


def lookup_char(probability, ranges):
    for char, range in enumerate(ranges):
        if range.x <= probability <= range.y:
            return char, range
    raise RuntimeError(f'Can not find char with probability = {probability}')


def decode(encoded_data: int):
    data_str = str(encoded_data)
    data_pointer = 0
    code = data_str[data_pointer:data_pointer + OPERATORS_SIZE]
    ranges, cr, delta = initialize()
    answer = bytearray()
    # prob = float('0.' + code)
    while True:
        prob = (int(code) - cr.x) / delta
        char, range = lookup_char(prob, ranges)
        if EOF == char:
            break
        answer.append(char)
        cr = recalculate_cr(cr, range)
        crs = cr.str()
        if crs.x[0] == crs.y[0]:
            cr = shift_cr(cr, crs)
            data_pointer += 1
            code = data_str[data_pointer:data_pointer + OPERATORS_SIZE]

    return answer


if __name__ == '__main__':
    # raw = b'abc'
    # encoded = encode(raw)
    # restored = decode(encoded)
    # print(raw == restored)
    swiss_miss = b'\x00\x01\x02\x00\x00\x04\x03\x02\x00\x00'  # SWISS_MISS 0120043200
    encoded = encode(swiss_miss)
    print(encoded)
    decoded = decode(encoded)
    print(decoded)
