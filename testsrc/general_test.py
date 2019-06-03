import os
from pathlib import Path
from typing import Union
from unittest import TestCase

from hufman.compressing.hufman_compress import compress_to_file, restore_from_file, compress_file, restore_file


def walk_files(path: Union[Path, str]):
    if not isinstance(path, Path):
        path = Path(path)

    if path.is_dir():
        for nested in path.iterdir():
            for iteration in walk_files(nested):
                yield iteration
    elif path.is_file():
        yield path


class GeneralTest(TestCase):

    def test_1(self):
        # base = 'D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources'
        # filename = 'wn.png'
        base = "D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources/files/EXE-файлы/DOS'овская программа Chemical Analysis"
        filename = '101.EXE'
        in_filename = os.path.join(base, filename)
        compr_filename = in_filename + '.hfm'
        out_filename = os.path.join(base, 'restored_' + filename)

        with open(in_filename, 'rb') as in_file:
            in_data = in_file.read()

        compress_to_file(in_data, compr_filename)

        rest_data = restore_from_file(compr_filename)
        with open(out_filename, 'wb') as out_file:
            out_file.write(rest_data)

    def test_all_passed_files_compress_restore_compare(self):
        for initial_filename in walk_files('D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources/files'):
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
            self.assertTrue(equal)
            print('\n------------------------------------------------\n\n')

