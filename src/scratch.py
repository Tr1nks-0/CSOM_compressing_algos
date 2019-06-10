from fractions import Fraction
from encoder.arithmetic.range import Range
from math import gcd

a = 0
b = 1
eof = 256

LEN = 257

Ra = Range(Fraction(0, LEN), Fraction(1, LEN))
Rb = Range(Fraction(1, LEN), Fraction(2, LEN))
Reof = Range(Fraction(256, LEN), Fraction(257, LEN))

inp = 'abba'

print('step0: "" + "a"')
CR0 = Range(Fraction(0), Fraction(1))
D0 = CR0.y - CR0.x
RCR0 = Range(D0 * Ra.x + CR0.x, D0 * Ra.y + CR0.x)

print('step 2: "a" + "b"')
CR1 = Range(RCR0.x, RCR0.y)
D1 = CR1.y - CR1.x
RCR1 = Range(D1 * Rb.x + CR1.x, D1 * Rb.y + CR1.x)
print(RCR1)

print('step 3: "ab" + "b"')
CR2 = Range(RCR1.x, RCR1.y)
D2 = CR2.y - CR2.x
RCR2 = Range(D2 * Rb.x + CR2.x, D2 * Rb.y + CR2.x)
print(RCR2)

print('step 4: "abb" + "a"')
CR3 = Range(RCR2.x, RCR2.y)
D3 = CR3.y - CR3.x
RCR3 = Range(D3 * Ra.x + CR3.x, D3 * Ra.y + CR3.x)
print(RCR3)

print('step eof: "abba" + "EOF"')
CReof = Range(RCR3.x, RCR3.y)
Deof = CReof.y - CReof.x
RCReof = Range(Deof * Reof.x + CReof.x, Deof * Reof.y + CReof.x)
print(RCReof)

print(f'Range: {RCReof}')

answer = RCReof
n = 0
denom = 1

while denom < answer.x.denominator:
    n += 1
    denom = denom << 1

print(f'n={n}, 2^n={denom}')

print(f'in length - {4 * 8} out length - {n}')
