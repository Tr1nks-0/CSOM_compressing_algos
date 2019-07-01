import math
import os
from typing import BinaryIO, Tuple

from encoder.encoder import Encoder
from encoder.hufman.tree.tree_node import Node
from encoder.hufman.tree.tree_utils import build_tree_from_bytes, tree_to_codetable, tree_to_bytes, tree_from_io


# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N1

# Реализация  метода сжатия Хаффмана
class HufmanEncoder(Encoder):
    def __init__(self):
        super().__init__()
        self.default_extension = 'hfm'
        self.name = 'Hufman'

    def compress_to_io(self, data: bytes, io: BinaryIO) -> tuple:
        data, meta = self.compress_to_bytes(data)
        io.write(data)
        return meta

    def restore_from_io(self, io: BinaryIO) -> bytes:
        hufman_tree, nodes_count = tree_from_io(io)
        if nodes_count == 0:
            return bytes()
        data = io.read()
        return self.restore_from_bytes(hufman_tree, data)

    # логика сжатия
    def compress_to_bytes(self, data: bytes) -> Tuple[bytes, tuple]:
        if len(data) == 0:
            return data, (0, 0)
        hufman_tree = build_tree_from_bytes(data)  # строим дерево
        code_table = tree_to_codetable(hufman_tree)  # получаем кодовую таблицу из дерева
        bit_str = '000'  # префикс дополнения бит справа, в конце содержит кол-во бит дополнения до байта
        for byte in data:  # побайтово идем по исходному файлу
            encoded = code_table.get(byte)  # и берем ключи Хаффмана для байт
            bit_str = bit_str + encoded  # Записываем их справа в строчную форму
        bit_count = len(bit_str)  # кол-во бит выходной последовательности
        reduced_bit_count = math.ceil(bit_count / 8) * 8  # ко-во бит приведенное до полных байт
        byte_complete_offset = reduced_bit_count - bit_count  # кол-во бит дополнения
        bit_str = bin(byte_complete_offset)[2:].zfill(3) + bit_str[3:] + '0' * byte_complete_offset  # дополненая до записи строка бит
        compressed = tree_to_bytes(hufman_tree) + bytes(int(bit_str[index:index + 8], 2) for index in range(0, len(bit_str), 8))  # полная кодовая запись с деревом и данными
        return compressed, self.calculate_meta(len(data), len(compressed))

    def restore_from_bytes(self, hufman_tree: Node, data: bytes) -> bytes:
        if len(data) == 0:
            return data
        reduced_bit_count = len(data) * 8  # кол-во бит во входной последовательности
        data_int = int.from_bytes(data, 'big')  # переводим входную последовательности в число
        data_bits = bin(data_int)[2:].zfill(reduced_bit_count)  # переводим число в биты и дополняем до исходного значения нулями слева
        byte_complete_offset = int(data_bits[:3], 2)  # смещение данных
        data_bits = data_bits[3:len(data_bits) - byte_complete_offset]  # биты закодированных данных
        restored_data = bytearray()
        node = hufman_tree  # корень дерева
        for bit_str in data_bits:  # побитово идем по файлу
            if bit_str == '1' and node.right_child:  # направо
                node = node.right_child
            elif node.left_child:  # налево
                node = node.left_child
            if node.is_data():
                restored_data.append(node.character)  # раскодировали, записываем
                node = hufman_tree  # корень в корень
        return restored_data
