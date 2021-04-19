import numpy as np
import os


class Sbox:
    """Manages the various SBOX substitutions required"""

    def __init__(self, sbox_filename:str):
        directory = os.path.dirname(__file__)
        filepath = os.path.join(directory, sbox_filename)
        self.sbox_matrix = np.loadtxt(filepath, dtype='S2')

    def sbox_substitution(self, hex_value):
        if len(str(hex_value)) <= 2:
            return self._short_sbox_substitution(hex_value)
        else:
            return self._long_sbox_substitution(hex_value)

    def _long_sbox_substitution(self, hex_value):

        raw_byte = str(hex_value)[2:]
        if len(raw_byte) == 3:
            nibble1 = int(raw_byte[0], 16)
            nibble2 = int(raw_byte[1], 16)
        else:
            nibble1 = 0
            nibble2 = int(raw_byte[0], 16)
        return self.sbox_matrix[nibble1, nibble2]

    def _short_sbox_substitution(self, hex_value):
        raw_byte = str(hex_value)

        if len(raw_byte) == 2:
            nibble1 = int(raw_byte[0], 16)
            nibble2 = int(raw_byte[1], 16)
        else:
            nibble1 = 0
            nibble2 = int(raw_byte[0], 16)
        return self.sbox_matrix[nibble1, nibble2]

    def matrix_sbox_substitution(self, hex_array: np.array) -> np.array:

        row1 = [self.sbox_substitution(hex_value) for hex_value in hex_array[0]]
        row2 = [self.sbox_substitution(hex_value) for hex_value in hex_array[1]]
        row3 = [self.sbox_substitution(hex_value) for hex_value in hex_array[2]]
        row4 = [self.sbox_substitution(hex_value) for hex_value in hex_array[3]]

        return np.array([row1, row2, row3, row4], dtype='S2')

