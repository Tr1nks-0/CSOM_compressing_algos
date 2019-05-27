import sys
from pathlib import Path


def help():
    print("""This is a util for compress files with Hufman algo.
\tUsage:
\tInteractive:"hufman"
\tAs command:\t"hufman -[flag] [input file]"
\tFlags:
\t\t -h --help         - interactive mode 
\t\t -c --compress     - compress mode
\t\t -r --restore      - restore mode
""")


EXIT_COMMANDS = ['q', 'e', 'quit', 'exit']


def __check_exit(arg) -> None:
    if arg in EXIT_COMMANDS:
        exit(0)


def interactive() -> None:
    loop = True
    while loop:
        print('For stop execution type exit.')
        mode = input('Enter ').lower()
        __check_exit(mode)
        file = input('Enter input file path').lower()
        __check_exit(file)
        process(mode, file)


def process(mode, file) -> None:
    if mode.strip('-') in ['c', 'compress']:
        compress_file(file)
    if mode.strip('-') in ['r', 'restore']:
        restore_file(file)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        interactive()
        exit(0)
    if 1 < len(sys.argv) < 3:
        print(f'Too few arguments. Expected 2 got {len(sys.argv) - 1}')
        exit(1)
    process(sys.argv[1], sys.argv[2])
