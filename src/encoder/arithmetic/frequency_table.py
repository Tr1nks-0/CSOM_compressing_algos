

# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N2
class FrequencyTable:

    def __init__(self, length):
        if length < 1:
            raise ValueError('Length should be at least 1.')

        self.frequencies = [1 for _ in range(length)]
        self.length = len(self.frequencies)
        self.amount = sum(self.frequencies)
        self.accumulated_frequency = self._recalculate_accumulated()

    def get(self, symbol):
        self._check_symbol(symbol)
        return self.frequencies[symbol]

    def set(self, symbol, frequency):
        self._check_symbol(symbol)
        if frequency < 0:
            raise ValueError("Negative frequency")
        different = self.amount - self.frequencies[symbol]
        self._check_different(different)
        self.amount = different + frequency
        self.frequencies[symbol] = frequency
        self.accumulated_frequency = self._recalculate_accumulated()

    def increment_char_frequency(self, symbol):
        self._check_symbol(symbol)
        self.amount += 1
        self.frequencies[symbol] += 1
        self.accumulated_frequency = self._recalculate_accumulated()

    def accumulated_x(self, symbol):
        self._check_symbol(symbol)
        return self.accumulated_frequency[symbol]

    def accumulated_y(self, symbol):
        self._check_symbol(symbol)
        return self.accumulated_frequency[symbol + 1]

    def _recalculate_accumulated(self) -> list:
        accumulated = [0]
        sum = 0
        for freq in self.frequencies:
            sum += freq
            accumulated.append(sum)
        return accumulated

    def _check_different(self, different):
        if different < 0:
            raise ValueError('Symbol frequency can not be greater than amount of frequencies')

    def _check_symbol(self, char):
        if 0 > char >= self.length:
            raise ValueError(f'Symbol {char} out of range')
