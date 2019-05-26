from os import path

from src.hufman.hufman_algo import compress_to_file, decompress_from_file

if __name__ == '__main__':
    basename = 'D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources'
    filename = 'wn.png'
    # filename = 'in'
    # filename = 'in_fib'

    input = path.join(basename, filename)
    output = path.join(basename, f'{filename}.hfm')
    restored = path.join(basename, f'restored_{filename}')

    with open(input, 'rb') as inp:
        input_data = inp.read()
        tree_1 = compress_to_file(input_data, output)

    restored_data = decompress_from_file(output, tree_1)
    with open(restored, 'wb') as out:
        out.write(restored_data)
    print(input_data)
    print(bytes(restored_data))
