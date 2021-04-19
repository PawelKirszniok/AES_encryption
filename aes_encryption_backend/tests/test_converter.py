from unittest import TestCase
import numpy as np
from aes_encryption_backend.converter import Converter
import os


class TestConverter(TestCase):

    def setUp(self):
        directory = os.path.dirname(__file__)
        bytes_file = os.path.join(directory, "test_bytes.txt")
        hex_file = os.path.join(directory, "test_hex.txt")
        array_file = os.path.join(directory, "test_array.txt")
        self.test_bytes = np.loadtxt(bytes_file, dtype=np.ubyte)
        self.test_hex = np.loadtxt(hex_file, dtype='S2')
        self.test_string = "abcdefgABCDEFG\n "
        self.test_array = np.loadtxt(array_file, dtype=np.ubyte)

    def test_byte_to_hex(self):
        self.assertTrue(np.array_equal(Converter.byte_to_hex(self.test_bytes), self.test_hex))

    def test_hex_to_byte(self):
        self.assertTrue(np.array_equal(Converter.hex_to_byte(self.test_hex), self.test_bytes))

    def test_make_array(self):
        self.assertTrue(np.array_equal(Converter.make_array(self.test_string), self.test_array))

    def test_make_string(self):
        self.assertEqual(Converter.make_string(self.test_array), self.test_string)
