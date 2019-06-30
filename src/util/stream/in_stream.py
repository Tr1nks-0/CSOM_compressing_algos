from typing import BinaryIO


# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N2
class BitInputStream:
    def __init__(self, source: BinaryIO):
        self.source = source
        self.has_next = True
        self.index = 0
        self.byte_int = 0
        self.has_next = True

    def read(self) -> int:
        if self.source.closed:
            raise IOError('Attempt to read from closed source stream')

        if self.index == 0:
            raw_byte = self.source.read(1)
            if len(raw_byte) == 0:
                self.has_next = False
                return -1

            self.index = 8
            self.byte_int = int.from_bytes(raw_byte, 'big')
        self.index -= 1
        return self.byte_int >> self.index & 1

    def bits(self):
        while self.has_next and not self.source.closed:
            bit = self.read()
            if bit >= 0:
                yield bit
            else:
                break

    def close(self) -> None:
        self.source.close()
        self.has_next = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
