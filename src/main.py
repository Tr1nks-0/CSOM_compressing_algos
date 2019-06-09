import sys

# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N1
from encoder.arithmetic.arithmetic_encoder import ArithmeticEncoder
from encoder.encoder import Encoder
from encoder.hufman.hufman_encoder import HufmanEncoder


def encoder_factory(algo_name: str) -> Encoder:
    if algo_name in ('h', 'hufman'):
        return HufmanEncoder()
    elif algo_name in ('a', 'arithmetic'):
        return ArithmeticEncoder()
    else:
        raise NotImplementedError(f'No algorithm with key {algo_name} found.')


def operate(encoder: Encoder, in_file_str, mode):
    filenames = in_file_str.split(',')
    for filename in filenames:
        if 'c' in mode:
            meta = encoder.compress_file(filename)
            print(f'File size reduced on {meta[0]} bytes. Compress rate: {meta[1]:.2f}%')
        if 'r' in mode:
            encoder.restore_file(filename)


if __name__ == '__main__':
    loop = True
    while (loop):
        if len(sys.argv) == 1:
            algo = input('Enter algorythm ( [H]ufman, [A]rithmetic ). For exit type [E]\n> ').lower()
            if algo == 'e' or algo == 'q':
                exit(0)
            mode = input('Enter operation type ( [C]ompress, [R]estore ). For exit type [E]\n> ').lower()
            if mode == 'e' or mode == 'q':
                exit(0)
            in_file_str = input('Enter filename\n> ')
        else:
            if 1 < len(sys.argv) < 4:
                print(f'To Few arguments for operate. Expected 3 : '
                      f'[algorithm] [operation] [input_file], got: {len(sys.argv)}\n')
                exit(1)
            loop = False
            mode = sys.argv[1]
            in_file_str = sys.argv[2]
        try:
            operate(encoder_factory(algo), in_file_str, mode)
        except FileNotFoundError:
            print(f'Can not find file : {in_file_str}')
            exit(1)
