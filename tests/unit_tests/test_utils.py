import unittest
import uttemplate

from cykhash.khashsets import float64_hash, float32_hash, int64_hash, int32_hash


class UtilsTester(unittest.TestCase): 
    def test_hash_float64_neg_zero(self):
        self.assertEqual(float64_hash(0.0), float64_hash(-0.0))


    def test_hash_float32_neg_zero(self):
        self.assertEqual(float32_hash(0.0), float32_hash(-0.0))


    def test_hash_float64_one(self):
        self.assertEqual(float64_hash(1.0), 536346624)


    def test_hash_float32_one(self):
        self.assertEqual(float32_hash(1.0), 1065353216)


    def test_hash_int64_zero(self):
        self.assertEqual(int64_hash(0), 0)


    def test_hash_int32_zero(self):
        self.assertEqual(int32_hash(0), 0)


    def test_hash_int64_one(self):
        self.assertEqual(int64_hash(1), 2049)


    def test_hash_int32_one(self):
        self.assertEqual(int32_hash(1), 1)




 
