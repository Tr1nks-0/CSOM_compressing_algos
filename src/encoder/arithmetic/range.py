from fractions import Fraction
from typing import Union


class Range:
    def __init__(self,
                 x: Union[Fraction, int, float] = Fraction(0),
                 y: Union[Fraction, int, float] = Fraction(0),
                 EOF=False):
        self.EOF = EOF
        self.x = x if isinstance(x, Fraction) else Fraction(x)
        self.y = y if isinstance(y, Fraction) else Fraction(y)

    def is_in_range(self, a: Union[Fraction, int, float]):
        if not isinstance(a, Fraction):
            a = Fraction(a)
        return self.x <= a < self.y

    def __repr__(self):
        return f'[{self.x} --- {self.y}]'
