import os
from unittest import TestCase

from hufman.compressing.hufman_compress import compress_to_file, restore_from_file


class GeneralTest(TestCase):

    def test_1(self):
        # base = 'D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources'
        # filename = 'wn.png'
        base = "D:/WORKSPACE/python/ControlSystemOptimizationMethods/resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/EXE-файлы/DOS'овская программа Chemical Analysis"
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
        filenames = [
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/EXE-файлы/DOS'овская программа Chemical Analysis/101.EXE",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/EXE-файлы/Linux 2.x e-mail программа PINE/pine.bin",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/EXE-файлы/Netscape Navigator v4.06 под Windows 95-98/netscape.exe",

            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/TXT-файлы/Anne of Green Gables by Lucy Maud Montgomery/anne11.txt",
            "D:\WORKSPACE\python\ControlSystemOptimizationMethods\resources\!!! ТЕСТОВЫЕ ФАЙЛЫ !!!\TXT-файлы\Английский перевод книги Три Мушкетера Александра Дюма\1musk10.txt",
            "D:\WORKSPACE\python\ControlSystemOptimizationMethods\resources\!!! ТЕСТОВЫЕ ФАЙЛЫ !!!\TXT-файлы\Книга Мировых Фактов ЦРУ 1995\world95.txt",

            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/_INST32I.EX_",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/_ISDEL.EXE",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/_SETUP.DLL",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/_sys1.cab",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/_user1.cab",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/codec.exe",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/DATA.TAG",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/data1.cab",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/lang.dat",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/layout.bin",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/os.dat",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/setup.bmp",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/SETUP.EXE",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/SETUP.INI",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/setup.ins",
            "resources/!!! ТЕСТОВЫЕ ФАЙЛЫ !!!/WORMS2 Test Files/setup.lid",

            "",
            "",
        ]
