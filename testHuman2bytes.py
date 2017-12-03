import unittest
import human2bytes

import os

class TestHuman2bytes(unittest.TestCase):

    def test_human2bytes(self):
        number_bytes = human2bytes.human2bytes("1 K")
        self.assertEqual(number_bytes, 1024)
        number_bytes = human2bytes.human2bytes("1K")
        self.assertEqual(number_bytes, 1024)
        number_bytes = human2bytes.human2bytes("5M")
        self.assertEqual(number_bytes, 5242880)
        number_bytes = human2bytes.human2bytes("5 G")
        self.assertEqual(number_bytes, 5368709120)
        number_bytes = human2bytes.human2bytes("1000")
        self.assertEqual(number_bytes, 1000)
        
if __name__ == '__main__':
    unittest.main()
