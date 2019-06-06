from decimal import Decimal
from typing import Union


class Range:
    def __init__(self,
                 x: Union[Decimal, int, float] = Decimal(0),
                 y: Union[Decimal, int, float] = Decimal(0),
                 EOF=False):
        self.EOF = EOF
        self.x = x if isinstance(x, Decimal) else Decimal(x)
        self.y = y if isinstance(y, Decimal) else Decimal(y)

    def is_in_range(self, a: Union[Decimal, int, float]):
        if not isinstance(a, Decimal):
            a = Decimal(a)
        return self.x <= a < self.y
