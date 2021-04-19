import numpy as np
from aes_encryption_backend.sbox import Sbox
from aes_encryption_backend.converter import Converter
import os


class AEScypher:
    """This class implements the AES 128 algorithm"""

    def __init__(self):

        self.sbox = Sbox("sbox.txt")
        self.inverse_sbox = Sbox("inverse_sbox.txt")
        directory = os.path.dirname(__file__)
        filepath = os.path.join(directory, "md5.txt")
        self.md5 = np.loadtxt(filepath, dtype=np.ubyte)
        self.padding_character = chr(255)

    def encode(self, key: str, plaintext: str) -> str:
        """encrypts any length text given a 16 byte or longer key"""
        print(plaintext)
        if len(key) > 16:
            key = key[:16]

        padding_required = (16 - len(plaintext) % 16) %16
        padding = ''.join([self.padding_character for _ in range(padding_required)])
        plaintext += padding

        nr_of_blocks = int(len(plaintext) / 16)
        blocks = []
        for block_number in range(nr_of_blocks):
            s = slice(block_number*16, (block_number+1)*16)
            blocks.append(plaintext[s])
        result = ''

        for block in blocks:
            result += self._encode_16(key, block)
        print(r"".format(result))
        print(len(result))
        return result

    def decode(self, key: str, cyphertext: str):
        """decrypts any length text given a 16 byte or longer key"""
        if len(key) > 16:
            key = key[:16]

        padding_required = (16 - len(cyphertext) % 16) % 16

        padding = ''.join([self.padding_character for _ in range(padding_required)])
        cyphertext += padding
        nr_of_blocks = int(len(cyphertext) / 16)
        blocks = []
        for block_number in range(nr_of_blocks):
            s = slice(block_number * 16, (block_number + 1) * 16)
            blocks.append(cyphertext[s])

        result = ''
        for block in blocks:
            result += self._decode_16(key, block)

        while result[-1] == self.padding_character:
            result = result[:-1]

        return result

    def _encode_16(self, key: str, plaintext: str) -> str:
        """encodes a 16 byte string """

        key_array = Converter.make_array(key)
        plaintext_array = Converter.make_array(plaintext)

        # generate round keys
        round_keys = self._generate_round_keys(Converter.byte_to_hex(key_array))

        # Add key0 to plaintext to start
        state_array = key_array ^ plaintext_array
        # main 9 round loop

        for round in range(1, 10):
            state_array = self._AES_encode_round(state_array, round_keys[round])

        # final round

        final_array = self._AES_encode_last_round(state_array, round_keys[10])
        return Converter.make_string(final_array)

    def _decode_16(self, key: str, cyphertext: str):
        """decodes a 16 byte string"""

        key_array = Converter.make_array(key)
        cyphertext_array = Converter.make_array(cyphertext)

        # generate round keys
        round_keys = self._generate_round_keys(Converter.byte_to_hex(key_array))
        # Add key0 to plaintext to start and first round
        state_array = round_keys[10] ^ cyphertext_array
        state_array = self._AES_decode_first_round(state_array)
        # main 9 round loop

        for i in range(1, 10):
            round = 10 - i
            state_array = self._AES_decode_round(state_array, round_keys[round])

        # final round
        state_array = Converter.hex_to_byte(state_array)

        final_array = state_array ^ key_array

        return Converter.make_string(final_array)

    def _AES_encode_round(self, state_array, round_key):
        """performs a typical round of encoding """
        hex_array = Converter.byte_to_hex(state_array)
        step1 = self.sbox.matrix_sbox_substitution(hex_array)
        step2 = self._shift_rows(step1)
        step2 = Converter.hex_to_byte(step2)
        step3 = self._mix_columns(step2)
        step4 = step3 ^ round_key

        return step4

    def _AES_decode_round(self, state_array, round_key):
        """reverses the steps of a signle encoding round"""
        step1 = Converter.hex_to_byte(state_array)
        step1 = step1 ^ round_key
        step2 = self._inverse_mix_columns(step1)
        step2 = Converter.byte_to_hex(step2)
        step3 = self._inverse_shift_rows(step2)
        step4 = self.inverse_sbox.matrix_sbox_substitution(step3)

        return step4

    def _AES_encode_last_round(self, state_array, round_key):
        """performs the last round of encoding"""
        hex_array = Converter.byte_to_hex(state_array)

        step1 = self.sbox.matrix_sbox_substitution(hex_array)
        step2 = self._shift_rows(step1)
        step2 = Converter.hex_to_byte(step2)
        step3 = step2 ^ round_key

        return step3

    def _AES_decode_first_round(self, state_array):
        """reverses the steps of the last encoding round"""
        step1 = Converter.byte_to_hex(state_array)
        step1 = self._inverse_shift_rows(step1)
        step2 = self.inverse_sbox.matrix_sbox_substitution(step1)

        return step2

    def _shift_rows(self, array:np.array) -> np.array:

        row1 = array[0]
        row2 = [array[1,1], array[1,2], array[1,3], array[1,0]]
        row3 = [array[2,2], array[2,3], array[2,0], array[2,1]]
        row4 = [array[3,3], array[3,0], array[3,1], array[3,2]]

        return np.array([row1, row2, row3, row4])

    def _inverse_shift_rows(self, array:np.array) -> np.array:

        row1 = array[0]
        row2 = [array[1,3], array[1,0], array[1,1], array[1,2]]
        row3 = [array[2,2], array[2,3], array[2,0], array[2,1]]
        row4 = [array[3,1], array[3,2], array[3,3], array[3,0]]

        return np.array([row1, row2, row3, row4])

    def _generate_round_keys(self, private_key: np.array) -> list:
        working_array = np.zeros((4, 44), dtype=np.ubyte)

        round_constants = [None, int('1', 16), int('2', 16), int('4', 16), int('8', 16), int('10', 16), int('20', 16)
            , int('40', 16), int('80', 16), int('1b', 16), int('36', 16)]

        for i in range(4):
            for j in range(4):
                working_array[i][j] = int(private_key[i][j], 16)

        for key_number in range(1, 11):
            for column_number in range(1, 5):
                if column_number == 1:
                    tmp_column = working_array[:, 4 * key_number + column_number - 2]
                    tmp_column = [tmp_column[1], tmp_column[2], tmp_column[3], tmp_column[0]]
                    tmp_column = [hex(item)[2:] for item in tmp_column]
                    tmp_column = [self.sbox.sbox_substitution(item) for item in tmp_column]
                    tmp_column = np.array([int(item, 16) for item in tmp_column], dtype=np.ubyte)

                    previous_column = working_array[:, 4 * key_number + column_number - 5]
                    tmp_column = previous_column ^ tmp_column ^ np.array(
                        [np.ubyte(round_constants[key_number]), np.ubyte(0), np.ubyte(0), np.ubyte(0)])
                    for i in range(4):
                        working_array[i][4 * key_number + column_number - 1] = tmp_column[i]
                else:
                    tmp_column = working_array[:, 4 * key_number + column_number - 2]
                    previous_column = working_array[:, 4 * key_number + column_number - 5]
                    tmp_column = previous_column ^ tmp_column
                    for i in range(4):
                        working_array[i][4 * key_number + column_number - 1] = tmp_column[i]

        return np.hsplit(working_array, 11)

    def _mix_columns(self, right_matrix: np.array) -> np.array:
        result = np.zeros((4, 4), dtype=np.ubyte)
        for row in range(4):
            for column in range(4):
                value1 = self._bitwise_multiply_operation(self.md5[row][0], right_matrix[0][column])
                value2 = self._bitwise_multiply_operation(self.md5[row][1], right_matrix[1][column])
                value3 = self._bitwise_multiply_operation(self.md5[row][2], right_matrix[2][column])
                value4 = self._bitwise_multiply_operation(self.md5[row][3], right_matrix[3][column])

                xor_sum = value1 ^ value2 ^ value3 ^ value4

                result[row][column] = xor_sum

        return result

    def _inverse_mix_columns(self, right_matrix: np.array) -> np.array:
        step1 = self._mix_columns(right_matrix)
        step2 = self._mix_columns(step1)
        step3 = self._mix_columns(step2)
        return step3

    @staticmethod
    def _bitwise_multiply_operation(multiplier, value):
        """implements bitwise multiplication by 1, 2 and 3"""

        if multiplier == 1:
            return value
        elif multiplier == 2:
            result = np.left_shift(value, 1)
            if result <= 255:
                return result
            else:
                return result ^ np.ubyte(27)
        elif multiplier == 3:
            result = np.left_shift(value, 1) ^ value
            if result <= 255:
                return result
            else:
                return result ^ np.ubyte(27)



if __name__ == "__main__":

    aes = AEScypher()

    cyphertext = aes._encode_16("Thats my Kung Fu", "Two One Nine Two")

    print(cyphertext)

    print(aes._decode_16("Thats my Kung Fu", cyphertext))

    cyphertext = aes.encode("Thats my Kung Fu", "16 Apr 2021, historic moment")

    print(cyphertext)

    print(aes.decode("Thats my Kung Fu", cyphertext))


