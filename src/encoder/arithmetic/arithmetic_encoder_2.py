class Range:
    def __init__(self, x, y):
        self.x = x
        self.y = y


EOF = 257


def _create_initial_ranges():
    probability = 1 / 258
    ranges = []
    for i in range(258):  # use 258 because it more dividable
        x = ranges[i - 1].y if i > 0 else 0
        y = x + probability
        ranges.insert(i, Range(x, y))
    return ranges


def encode(data: bytes):
    """
    works in right of decimal point e.g. :
    decimal : 0.79648
      works :   79684


    @:return decimal part of encoded data e.g. if encoded = 0.1245785 it returns 1245785
    """
    ranges = _create_initial_ranges()
    cr = Range(00000000,
               99999999)

    answer = 0
    for char in data:
        rn = ranges[char]
        delta = cr.y - cr.x + 1  # +1 because here we use absolet cr.y value, not going to int but "int" e.g 0.999999 goes to 1000000
        cr.y = int(cr.x + delta * rn.y - 1)  # RCRy=CRx+delta*Ry-1  # -1 because we are going to int number but always less a bit e.g 1 is representing like 0.99999999
        cr.x = int(cr.x + delta * rn.x)  # RCRx=CRx+delta*Rx  # -1

        crx_str = str(cr.x)
        cry_str = str(cr.y)
        if crx_str[0] == cry_str[0]:
            answer = answer * 10 + int(crx_str[0])
            cr.x = int(crx_str[1:])
            cr.y = int(cry_str[1:])

    delta = cr.y - cr.x + 1
    rn = ranges[EOF]
    cr.x = int(cr.x + delta * rn.x)

    crx_str = str(cr.x)
    answer = answer * len(crx_str) + int(crx_str)

    return answer


if __name__ == '__main__':
    inp = b'abc'
    enc = encode(inp)
    print(bin(int.from_bytes(inp,'big'))[2:])
    print(bin(enc)[2:])
    print(enc)
