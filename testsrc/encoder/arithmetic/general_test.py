from pathlib import Path
from typing import Union
from unittest import TestCase

from encoder.arithmetic.adaptive_encoder import AdaptiveArithmeticEncoder


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

    def test_all_passed_files_compress_restore_compare(self):
        files_dir = Path(__file__).parents[3] / 'resources' / 'files'
        for initial_filename in walk_files(files_dir):
            print(initial_filename)
            encoder = AdaptiveArithmeticEncoder()
            meta = encoder.compress_file(initial_filename)
            print(f'File size reduced on {meta[0]} bytes. Compress rate: {meta[1]:.2f}%')

            encoder = AdaptiveArithmeticEncoder()
            compressed_filename = str(initial_filename) + '.arth'
            restored_filename = encoder.restore_file(compressed_filename)

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
