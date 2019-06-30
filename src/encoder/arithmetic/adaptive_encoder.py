from io import BytesIO
from typing import BinaryIO, Tuple, IO

from encoder.arithmetic.encoder_base import ArithmeticEncoder, ArithmeticDecoder
from encoder.arithmetic.frequency_table import FrequencyTable
from encoder.encoder import Encoder
from util.stream.in_stream import BitInputStream
from util.stream.out_stream import BitOutputStream

# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N2
class AdaptiveArithmeticEncoder(Encoder):
    def __init__(self):
        super().__init__()
        self.default_extension = 'arth'
        self.name = 'Arithmetic'
        self.frequencies = FrequencyTable(257)

    def compress_to_io(self, data: bytes, io: BinaryIO) -> Tuple[int, float, str]:
        compressed = BytesIO()
        input = BytesIO(data)
        with BitOutputStream(compressed) as bit_out:
            self.compress(input, bit_out)
            compressed_length = compressed.getbuffer().nbytes
            io.write(compressed.getvalue())
        return self.calculate_meta(len(data), compressed_length)

    def restore_from_io(self, io: BinaryIO) -> bytes:
        restored = BytesIO()
        with BitInputStream(io) as bin_in:
            self.decompress(bin_in, restored)
        return restored.getvalue()

    def compress(self, input: IO, bit_output: BitOutputStream):
        enc = ArithmeticEncoder(32, bit_output)
        while True:
            symbol = input.read(1)
            if len(symbol) == 0:
                break
            symbol = symbol[0]
            enc.write(self.frequencies, symbol)
            self.frequencies.increment_char_frequency(symbol)
        enc.write(self.frequencies, 256)
        enc.finish()

    def decompress(self, bit_input: BitInputStream, output: IO):
        dec = ArithmeticDecoder(32, bit_input)
        while True:
            symbol = dec.read(self.frequencies)
            if symbol == 256:
                break
            output.write(bytes((symbol,)))
            self.frequencies.increment_char_frequency(symbol)
