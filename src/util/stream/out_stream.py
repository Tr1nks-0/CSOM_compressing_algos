from typing import BinaryIO


class BitOutputStream:
    def __init__(self, destination: BinaryIO):
        self.destination = destination
        self.buffer_byte = 0
        self.buffer_length = 0

    def write(self, bit: int):
        if 1 < bit < 0:
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
        self.destination.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()