from unittest import TestCase
from aes_encryption_backend.AES_cypher import AEScypher

class TestAEScypher(TestCase):

    def setUp(self) -> None:
        self.AES = AEScypher()
        self.plaintext_short="\n test 1 $"
        self.plaintext_long = "this is a long test string 123456 !"
        self.key = "this is a test key"
        self.cyphertext_short = "r¿}b^½­4¡¶JLx"
        self.cyphertext_long = "ß-ÈN:ê$VÎZ\nøÇmÿO;O;ðù6aä4üßC Ê xÅ\S"

    def test_encrypt(self):
        # Test Short Text
        self.assertEqual(self.AES.encode(self.key, self.plaintext_short), self.cyphertext_short)

        # Test Long Text
        self.assertEqual(self.AES.encode(self.key, self.plaintext_long), self.cyphertext_long)

    def test_decrypt(self):
        # Test Short Cyphertext
        self.assertEqual(self.AES.decode(self.key, self.cyphertext_short), self.plaintext_short)

        #Test Long Cyphertext
        self.assertEqual(self.AES.decode(self.key, self.cyphertext_long), self.plaintext_long)


