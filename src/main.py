import sys

# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N1 N2
from encoder.arithmetic.adaptive_encoder import AdaptiveArithmeticEncoder
from encoder.encoder import Encoder
from encoder.hufman.hufman_encoder import HufmanEncoder


# фабрика алгоритмов
def encoder_factory(algo_name: str) -> Encoder:
    if algo_name in ('h', 'hufman'):
        return HufmanEncoder()
    elif algo_name in ('a', 'arithmetic'):
        return AdaptiveArithmeticEncoder()
    else:
        raise NotImplementedError(f'No algorithm with key {algo_name} found.')


# обработать файл с помошью алгоритма
def operate(encoder: Encoder, in_file_str, mode):
    filenames = in_file_str.split(',')
    for filename in filenames:
        if 'c' in mode:
            meta = encoder.compress_file(filename)
            print(f'File size reduced on {meta[0]} bytes. Compress rate: {meta[1]:.2f}%')
        if 'r' in mode:
            encoder.restore_file(filename)


# Точка начала исполнение скрипта
if __name__ == '__main__':
    loop = True
    while (loop):
        if len(sys.argv) == 1:  # запуск в интеактивном режиме
            algo = input('Enter algorythm ( [H]ufman, [A]rithmetic ). For exit type [E]\n> ').lower()
            if algo == 'e' or algo == 'q':
                exit(0)
            mode = input('Enter operation type ( [C]ompress, [R]estore ). For exit type [E]\n> ').lower()
            if mode == 'e' or mode == 'q':
                exit(0)
            in_file_str = input('Enter filename\n> ')
        else:  # запуск в коммандном режиме
            if 1 < len(sys.argv) < 4:
                print(f'To Few arguments for operate. Expected 3 : '
                      f'[algorithm] [operation] [input_file], got: {len(sys.argv)}\n')
                exit(1)
            loop = False
            algo = sys.argv[1]
            mode = sys.argv[2]
            in_file_str = sys.argv[3]
        try:
            operate(encoder_factory(algo), in_file_str, mode)
        except FileNotFoundError:
            print(f'Can not find file : {in_file_str}')
            exit(1)
