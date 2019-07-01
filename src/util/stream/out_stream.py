from typing import BinaryIO


# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N2
class BitOutputStream:
    def __init__(self, destination: BinaryIO):
        self.destination = destination
        self.buffer_byte = 0
        self.buffer_length = 0

    def write(self, bit: int):
        if bit not in (0, 1):
            raise ValueError(f'Bit should be 0 or 1, Not {bit}')
        self.buffer_byte = self.buffer_byte << 1 | bit
        self.buffer_length += 1
        if self.buffer_length == 8:
            self.destination.write(self.buffer_byte.to_bytes(1, 'big'))
            self.buffer_byte = 0
            self.buffer_length = 0
        elif self.buffer_length > 8:
            raise RuntimeError('Something went wrong with output stream - complete byte was not wrote.')

    def close(self):
        self.flush()
        self.destination.close()

    def flush(self):
        while self.buffer_length != 0:
            self.write(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
