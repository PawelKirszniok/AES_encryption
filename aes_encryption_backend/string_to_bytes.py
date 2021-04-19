import numpy as np
import logging

class StringToBytesConverter:

    conversion_table:{}

    def string_to_bytes(self):
        pass


def make_array(input_string: str) -> np.array:
    byte_conversion = bytearray(input_string, "ASCII")
    row1 = [byte_conversion[0], byte_conversion[4], byte_conversion[8], byte_conversion[12]]
    row2 = [byte_conversion[1], byte_conversion[5], byte_conversion[9], byte_conversion[13]]
    row3 = [byte_conversion[2], byte_conversion[6], byte_conversion[10], byte_conversion[14]]
    row4 = [byte_conversion[3], byte_conversion[7], byte_conversion[11], byte_conversion[15]]

    new_array = np.array([row1, row2, row3, row4], dtype=np.ubyte)
    print(new_array)
    return new_array

def byte_to_hex(byte_array:np.array) -> np.array:
    row1 = [hex(byte_value)[2:] for byte_value in byte_array[0]]
    row2 = [hex(byte_value)[2:] for byte_value in byte_array[1]]
    row3 = [hex(byte_value)[2:] for byte_value in byte_array[2]]
    row4 = [hex(byte_value)[2:] for byte_value in byte_array[3]]

    new_hex_array = np.array([row1, row2, row3, row4], dtype='S2')
    return new_hex_array


def hex_to_byte(hex_array:np.array) -> np.array:
    row1 = [int(hex_value, 16) for hex_value in hex_array[0]]
    row2 = [int(hex_value, 16) for hex_value in hex_array[1]]
    row3 = [int(hex_value, 16) for hex_value in hex_array[2]]
    row4 = [int(hex_value, 16) for hex_value in hex_array[3]]

    new_byte_array = np.array([row1, row2, row3, row4], dtype=np.ubyte)
    print(type(new_byte_array[1][1]))
    return new_byte_array


def sbox_substitution(hex_value):
    sbox = np.loadtxt("sbox.txt", dtype='S2')
    raw_byte = str(hex_value)[2:]
    if len(raw_byte) == 3:
        nibble1 = int(raw_byte[0], 16)
        nibble2 = int(raw_byte[1], 16)
    else:
        nibble1 = 0
        nibble2 = int(raw_byte[0], 16)
    return sbox[nibble1, nibble2]


def short_sbox_substitution(hex_value):
    sbox = np.loadtxt("sbox.txt", dtype='S2')
    raw_byte = str(hex_value)
    if len(raw_byte) == 2:
        nibble1 = int(raw_byte[0], 16)
        nibble2 = int(raw_byte[1], 16)
    else:
        nibble1 = 0
        nibble2 = int(raw_byte[0], 16)
    return sbox[nibble1, nibble2]


def matrix_sbox_substitution(hex_array:np.array) -> np.array:
    row1 = [sbox_substitution(hex_value) for hex_value in hex_array[0]]
    row2 = [sbox_substitution(hex_value) for hex_value in hex_array[1]]
    row3 = [sbox_substitution(hex_value) for hex_value in hex_array[2]]
    row4 = [sbox_substitution(hex_value) for hex_value in hex_array[3]]

    return np.array([row1, row2, row3, row4], dtype='S2')


def shift_row(array:np.array) -> np.array:

    row1 = array[0]
    row2 = [array[1,1], array[1,2], array[1,3], array[1,0]]
    row3 = [array[2,2], array[2,3], array[2,0], array[2,1]]
    row4 = [array[3,3], array[3,0], array[3,1], array[3,2]]

    return np.array([row1, row2, row3, row4])


def bitwise_multiply_operation(multiplier, value):
    print(int(value))

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


def matrix_multiply_4x4(left_matrix:np.array, right_matrix:np.array)->np.array:
    result = np.zeros((4, 4), dtype=np.ubyte)
    for row in range(4):
        for column in range(4):
            value1 = bitwise_multiply_operation(left_matrix[row][0], right_matrix[0][column])
            value2 = bitwise_multiply_operation(left_matrix[row][1], right_matrix[1][column])
            value3 = bitwise_multiply_operation(left_matrix[row][2], right_matrix[2][column])
            value4 = bitwise_multiply_operation(left_matrix[row][3], right_matrix[3][column])

            tmp = value1 ^ value2 ^ value3 ^ value4

            result[row][column] = tmp

    return result


def generate_round_keys(private_key:np.array) -> list:
    working_array = np.zeros((4, 44), dtype=np.ubyte)

    round_constants = [None, int('1', 16), int('2', 16), int('4', 16), int('8', 16), int('10', 16), int('20', 16)
                        , int('40', 16), int('80', 16), int('1b', 16), int('36', 16)]

    for i in range(4):
        for j in range(4):
            print(private_key[i][j])
            print(type(private_key[i][j]))
            working_array[i][j] = int(private_key[i][j], 16)
            print(f'{working_array[i][j]}+{type(working_array[i][j])}')

    for key_number in range(1, 11):
        for column_number in range(1, 5):
            if column_number == 1:
                tmp_column = working_array[:,4*key_number+column_number-2]
                tmp_column = [tmp_column[1], tmp_column[2], tmp_column[3], tmp_column[0]]
                tmp_column = [hex(item)[2:] for item in tmp_column]
                print(f'before substitution {tmp_column}')
                tmp_column = [short_sbox_substitution(item) for item in tmp_column]
                print(f'after substitution {tmp_column}')
                tmp_column = np.array([int(item, 16) for item in tmp_column], dtype=np.ubyte)

                previous_column = working_array[:, 4*key_number+column_number-5]
                print(f'previous column {[hex(item)[2:] for item in previous_column]}')
                tmp_column = previous_column ^ tmp_column ^ np.array([np.ubyte(round_constants[key_number]), np.ubyte(0), np.ubyte(0), np.ubyte(0)])
                print(f'xor {[hex(item)[2:] for item in tmp_column]}')
                for i in range(4):
                    working_array[i][4*key_number+column_number-1] = tmp_column[i]
            else:
                tmp_column = working_array[:, 4 * key_number + column_number - 2]
                previous_column = working_array[:, 4 * key_number + column_number - 5]
                tmp_column = previous_column ^ tmp_column
                for i in range(4):
                    working_array[i][4*key_number+column_number-1] = tmp_column[i]
                

    return np.hsplit(working_array, 11)




if __name__ == "__main__":

    test_int = np.ubyte(84)

    test_hex = hex(test_int)[2:]
    print(len(test_hex))
    print(test_hex)

    second_test_int = np.ubyte(int(test_hex, 16))

    print(second_test_int)

    test_string = "Thats my Kung Fu"

    test_plaintext = "Two One Nine Two"

    test_array1 = make_array(test_string)
    test_array2 = make_array(test_plaintext)
    test_xor = test_array1 ^ test_array2
    print(test_xor)
    hex_array = byte_to_hex(test_xor)
    print(hex_array)

    item = str(hex_array[1, 1])[2:]

    print(len(str(hex_array[2,0])))
    raw_byte = str(hex_array[2,0])[2:]
    print(raw_byte)
    print(len(raw_byte))
    if len(raw_byte) == 3:
        nibble1 = int(raw_byte[0], 16)
        nibble2 = int(raw_byte[1], 16)
    else:
        nibble1 = 0
        nibble2 = nibble1 = int(raw_byte[0], 16)
    print(nibble1)
    print(nibble2)
    print(sbox_substitution(hex_array[2,0]))

    print(f'item [2,2] = {item}, type - {type(item)} so {item[0]}-{item[1]}')

    sbox_array = matrix_sbox_substitution(hex_array)
    print(sbox_array)
    print(f'sbox[2] = \n {sbox_array[2]}')

    shifted_array = shift_row(sbox_array)

    print(shifted_array)

    md5 = np.loadtxt("md5.txt", dtype=np.ubyte)

    print(md5)
    shifted_numeric_array = hex_to_byte(shifted_array)

    column_mixed_array = matrix_multiply_4x4(md5, shifted_numeric_array)
    print(column_mixed_array)

    hex_column_mixed = byte_to_hex(column_mixed_array)
    print(hex_column_mixed)

    print("roundkeys \n ")
    round_key_stack = generate_round_keys(byte_to_hex(test_array1))

    for array in round_key_stack:
        print(byte_to_hex(array))
