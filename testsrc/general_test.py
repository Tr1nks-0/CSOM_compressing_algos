import os
from unittest import TestCase

from hufman.compressing.hufman_compress import compress_to_file, restore_from_file


class GeneralTest(TestCase):

    def test_1(self):
        base = 'D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources'
        filename = 'wn.png'
        in_filename = os.path.join(base, filename)
        compr_filename = in_filename + '.hfm'
        out_filename = os.path.join(base, 'restored_' + filename)

        with open(in_filename, 'rb') as in_file:
            in_data = in_file.read()
            print(in_data)

        compress_to_file(in_data, compr_filename)

        rest_data = restore_from_file(compr_filename)
        print(rest_data)
        with open(out_filename, 'wb') as out_file:
            out_file.write(rest_data)
