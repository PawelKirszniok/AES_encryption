from unittest import TestCase
from aes_encryption_backend.sbox import Sbox
import numpy as np


class TestSbox(TestCase):
    def setUp(self) -> None:
        self.sbox = Sbox("sbox.txt")

    def test_sbox_substitution(self):
        a = b'a1'
        b = b'32'
        self.assertEqual(self.sbox.sbox_substitution(a), b)

    def test__long_sbox_substitution(self):
        test_array_a = np.loadtxt("test_hex.txt", dtype='S2')
        test_array_b = np.loadtxt("test_sbox.txt", dtype='S2')

        self.assertTrue(np.array_equal(self.sbox.matrix_sbox_substitution(test_array_a), test_array_b))
