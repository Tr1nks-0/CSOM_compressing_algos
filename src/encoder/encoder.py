# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N1 N2
import os
from typing import BinaryIO, Tuple


# Класс содержащий базовые методы по сжатию и восстановлению. Используется как абстрактный рродитель конкретных алгоритмов
class Encoder:

    def __init__(self):
        self.default_extension = 'NotImplemented'
        self.name = 'Generic encoder'

    # Сжать файл в новый файл, будет выбрано уникальное для текущей директории имя
    def compress_file(self, filename: str) -> Tuple[int, float, str]:
        with open(filename, 'rb') as input_file:
            data = input_file.read()
            return self.compress_to_file(data, f'{str(filename)}.{self.default_extension}')

    # Восстановить фийл в файл, имя будет приведено к имени файла до сжатия
    def restore_file(self, filename: str) -> str:
        restored_filename = self.__resolve_restored_filename(filename)
        restored = self.restore_from_file(filename)
        with open(restored_filename, 'wb') as file:
            file.write(restored)
        return restored_filename

    # Сжать данные в файл
    def compress_to_file(self, data: bytes, filename: str) -> Tuple[int, float, str]:
        with open(filename, 'wb') as file:
            return self.compress_to_io(data, file)

    # Восстановить из файла в массив байт
    def restore_from_file(self, filename: str) -> bytes:
        with open(filename, 'rb') as file:
            return self.restore_from_io(file)

    # сжать и записать в поток
    def compress_to_io(self, data: bytes, io: BinaryIO) -> Tuple[int, float, str]:
        raise NotImplementedError('Generic class implementation called')

    # восстановить из потока
    def restore_from_io(self, io: BinaryIO) -> bytes:
        raise NotImplementedError('Generic class implementation called')

    # подсчитать степень сжатия файла путем сравнения объемов исходного и сжатого файлов. Приводится к %
    def calculate_meta(self, initial_length, compressed_length) -> Tuple[int, float, str]:
        size_different = initial_length - compressed_length
        rate = 100 - compressed_length / (1 if initial_length == 0 else initial_length) * 100
        return size_different, rate, self.name

    def __resolve_restored_filename(self, input_filename) -> str:
        dir, filename = os.path.split(input_filename)
        file, ext = os.path.splitext(filename)
        if ext == f'.{self.default_extension}':
            file, ext = os.path.splitext(file)
        name = os.path.join(dir, file + ext)
        i = 1
        while os.path.exists(name):
            name = os.path.join(dir, file + f'-({i})' + ext)
            i += 1
        return name
