from pathlib import Path

from hufman.compressing.hufman_compress import compress_file, restore_file


def test_ttt():
    # initial_filename = Path('D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources/files/Разноформатные файлы/The Artificial Corpus/a.txt')
    # initial_filename = Path('D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources/files/EXE-файлы/Netscape Navigator v4.06 под Windows 95-98/netscape.exe')
    # initial_filename = Path("D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources/files/EXE-файлы/DOS'овская программа Chemical Analysis/101.EXE")
    # initial_filename = Path("D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources/files/EXE-файлы/Linux 2.x e-mail программа PINE/pine.bin")
    initial_filename = Path("D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources/files/TXT-файлы/Книга Мировых Фактов ЦРУ 1995/world95.txt")
    print(initial_filename)
    meta = compress_file(initial_filename)
    print(f'File size reduced on {meta[0]} bytes. Compress rate: {meta[1]:.2f}%')

    compressed_filename = str(initial_filename) + '.hfm'
    restored_filename = restore_file(compressed_filename)

    with open(initial_filename, 'rb') as initial, open(restored_filename, 'rb') as restored:
        initial_data = initial.read()
        restored_data = restored.read()
    equal = initial_data == restored_data
    if equal:
        print('SUCCESS: Initial and compressed&restored file content are identical')
        Path(compressed_filename).unlink()
        Path(restored_filename).unlink()
    else:
        print('FAILTURE')
        # print('init:', initial_data)
        # print('rest:', restored_data)

if __name__ == '__main__':
    test_ttt()