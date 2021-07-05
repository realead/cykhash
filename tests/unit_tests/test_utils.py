from unittestmock import UnitTestMock

from cykhash.utils import float64_hash, float32_hash, int64_hash, int32_hash, object_hash, objects_are_equal

from cykhash.compat import assert_if_not_on_PYPY

class TestUtils(UnitTestMock): 
    def test_hash_float64_neg_zero(self):
        self.assertEqual(float64_hash(0.0), float64_hash(-0.0))


    def test_hash_float32_neg_zero(self):
        self.assertEqual(float32_hash(0.0), float32_hash(-0.0))


    def test_hash_float64_one(self):
        self.assertEqual(float64_hash(1.0), 1954243739)


    def test_hash_float32_one(self):
        self.assertEqual(float32_hash(1.0), 1648074928)


    def test_hash_int64_zero(self):
        self.assertEqual(int64_hash(0), 4178429809)


    def test_hash_int32_zero(self):
        self.assertEqual(int32_hash(0), 649440278)


    def test_hash_int64_one(self):
        self.assertEqual(int64_hash(1), 1574219535)


    def test_hash_int32_one(self):
        self.assertEqual(int32_hash(1), 1753268367)


    def test_hash_object_zero(self):
        self.assertEqual(object_hash(0), 0)


    def test_hash_object_one(self):
        self.assertEqual(object_hash(1), 2049)


    def test_equal_tupples_with_nan(self):
        t1 = (1, (float("nan"), 2), (4, (float("nan"),)))
        t2 = (1, (float("nan"), 2), (4, (float("nan"),)))
        assert_if_not_on_PYPY(t1 != t2, "nan is a singleton on PyPy")
        assert objects_are_equal(t1, t2)
 
