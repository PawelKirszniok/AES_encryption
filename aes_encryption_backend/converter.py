import numpy as np


class Converter:
    """Carries out conversions required for computations"""

    @staticmethod
    def byte_to_hex(byte_array: np.array) -> np.array:
        row1 = [hex(byte_value)[2:] for byte_value in byte_array[0]]
        row2 = [hex(byte_value)[2:] for byte_value in byte_array[1]]
        row3 = [hex(byte_value)[2:] for byte_value in byte_array[2]]
        row4 = [hex(byte_value)[2:] for byte_value in byte_array[3]]

        new_hex_array = np.array([row1, row2, row3, row4], dtype='S2')
        return new_hex_array

    @staticmethod
    def hex_to_byte(hex_array: np.array) -> np.array:
        row1 = [int(hex_value, 16) for hex_value in hex_array[0]]
        row2 = [int(hex_value, 16) for hex_value in hex_array[1]]
        row3 = [int(hex_value, 16) for hex_value in hex_array[2]]
        row4 = [int(hex_value, 16) for hex_value in hex_array[3]]

        new_byte_array = np.array([row1, row2, row3, row4], dtype=np.ubyte)
        return new_byte_array

    @staticmethod
    def make_array(input_string: str) -> np.array:
        byte_conversion = [ord(character) for character in input_string]
        row1 = [byte_conversion[0], byte_conversion[4], byte_conversion[8], byte_conversion[12]]
        row2 = [byte_conversion[1], byte_conversion[5], byte_conversion[9], byte_conversion[13]]
        row3 = [byte_conversion[2], byte_conversion[6], byte_conversion[10], byte_conversion[14]]
        row4 = [byte_conversion[3], byte_conversion[7], byte_conversion[11], byte_conversion[15]]

        new_array = np.array([row1, row2, row3, row4], dtype=np.ubyte)
        return new_array

    @staticmethod
    def make_string(input_array:np.array) ->str:
        result = []
        for column in range(4):
            for row in range(4):
                byte = chr(int(input_array[row][column]))
                result.append(byte)

        return ''.join(result)


