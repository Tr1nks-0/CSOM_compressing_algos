from os import path

from src.hufman.hufman_algo import compress_to_file, decompress_from_file

if __name__ == '__main__':
    basename = 'C:/W/controlsSystemOptimisationMethods/resources'
    filename = 'wn.png'
    # filename = 'in'
    # filename = 'in_fib'

    compressed_filename = f'{filename}.hfm'
    restored_filename = f'restored_{filename}'
    input = path.join(basename, filename)
    output = path.join(basename, compressed_filename)
    restored = path.join(basename, restored_filename)

    with open(input, 'rb') as inp:
        input_data = inp.read()
        compress_to_file(input_data, compressed_filename)

    restored_data = decompress_from_file(compressed_filename)
    with open(restored, 'wb') as out:
        out.write(restored_data)
    print(input_data)
    print(bytes(restored_data))
