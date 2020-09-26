import unittest
import uttemplate

from cykhash.khashsets import float64_hash, float32_hash


class UtilsTester(unittest.TestCase): 
    def test_hash_float64_neg_zero(self):
        self.assertEqual(float64_hash(0.0), float64_hash(-0.0))


    def test_hash_float32_neg_zero(self):
        self.assertEqual(float32_hash(0.0), float32_hash(-0.0))


    def test_hash_float64_one(self):
        self.assertEqual(float64_hash(1.0), 536346624)


    def test_hash_float32_one(self):
        self.assertEqual(float32_hash(1.0), 1065353216)



 
