import sys

from encoder.hufman.hufman_compress import compress_file, restore_file


def compress(filename):
    pass


def restore(filename):
    pass


def operate(in_file_str, mode):
    filenames = in_file_str.split(',')
    for filename in filenames:
        if 'c' in mode:
            meta = compress_file(filename)
            print(f'File size reduced on {meta[0]} bytes. Compress rate: {meta[1]:.2f}%')
        if 'r' in mode:
            restore_file(filename)


if __name__ == '__main__':
    loop = True
    while (loop):
        if len(sys.argv) == 1:
            mode = input('Enter operation type ( [C]ompress, [R]estore ). For exit type [E]\n> ').lower()
            if mode == 'e' or mode == 'q':
                exit(0)
            in_file_str = input('Enter filename\n> ')
        else:
            if 1 < len(sys.argv) < 3:
                print(f'To Few arguments for operate. Expected 2 : [operation] [input_file], got: {len(sys.argv)}\n')
                exit(1)
            loop = False
            mode = sys.argv[1]
            in_file_str = sys.argv[2]
        try:
            operate(in_file_str, mode)
        except FileNotFoundError:
            print(f'Can not find file : {in_file_str}')
            exit(1)
