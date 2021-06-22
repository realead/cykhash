import pytest
from unittestmock import UnitTestMock

import struct

from cykhash import Int64to64Map, Int32to32Map, Float64to64Map, Float32to32Map, PyObjectMap


@pytest.mark.parametrize(
    "map_type",
    [
        Int64to64Map, Int32to32Map, Float64to64Map, Float32to32Map,
    ],
)
class TestCommonMap(UnitTestMock): 

   def test_created_empty(self, map_type):
      s=map_type()
      self.assertEqual(len(s), 0)

   def test_put_int_once(self, map_type):
      s=map_type()
      s[1] = 43
      self.assertEqual(len(s), 1)
      self.assertEqual(s[1], 43)

   def test_put_int_twice(self, map_type):
      s=map_type()
      s[1] = 43
      s[1] = 43
      self.assertEqual(len(s), 1)
      self.assertEqual(s[1], 43)

   def test_add_two(self, map_type):
      s=map_type()
      s[1] = 43
      s[2] = 44
      self.assertEqual(len(s), 2)
      self.assertEqual(s[1], 43)
      self.assertEqual(s[2], 44)

   def test_add_many_twice(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       s[i] = 44
       self.assertEqual(len(s), i+1)
     #no changes for the second insert:
     for i in range(N):
       s[i] = 44
       self.assertEqual(len(s), N)


   def test_contains_none(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       self.assertFalse(i in s)


   def test_contains_all(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       s[i] = i+1
     for i in range(N):
       self.assertTrue(i in s)

   def test_contains_odd(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       if i%2==1:
        s[i] = i+1
     for i in range(N):
       self.assertEqual(i in s, i%2==1)

   def test_contains_even(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       if i%2==0:
        s[i] = i+1
     for i in range(N):
       self.assertEqual(i in s, i%2==0)


   def test_delete_even(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       s[i] = i+1
 
     #delete even:
     for i in range(N):
       if i%2==0:
          n=len(s)
          s.discard(i)
          self.assertEqual(len(s), n-1)
          s.discard(i)
          self.assertEqual(len(s), n-1)

     #check odd is still inside:
     for i in range(N):
        self.assertEqual(i in s, i%2==1)

   def test_zero_hint_ok(self, map_type):
      s = map_type(number_of_elements_hint=0)
      s[4] = 7
      s[5] = 7
      self.assertTrue(4 in s)
      self.assertTrue(5 in s)

   def test_as_int64_a_float(self, map_type):
      s = map_type(number_of_elements_hint=20, for_int=True)
      s[4] = 5.4
      self.assertEqual(s[4], 5)

   def test_as_int64_put_get(self, map_type):
      s = map_type(number_of_elements_hint=20, for_int=True)
      s[4] = 5
      self.assertEqual(s[4], 5)

   def test_as_float64_put_get(self, map_type):
      s = map_type(number_of_elements_hint=20, for_int=False)
      s[4] = 5
      self.assertEqual(s[4], 5)


@pytest.mark.parametrize(
    "map_type",
    [
        Float64to64Map, Float32to32Map, PyObjectMap,
    ],
)
class TestFloat(UnitTestMock): 
    def test_nan_right(self, map_type):
        NAN=float("nan")
        s=map_type()
        self.assertFalse(NAN in s)
        s[NAN] = 1
        self.assertTrue(NAN in s)
 
#+0.0/-0.0 will break when there are more than 2**32 elements in the map
# bacause then hash-function will put them in different buckets 

    def test_signed_zero1(self, map_type):
        MINUS_ZERO=float("-0.0")
        PLUS_ZERO =float("0.0")
        self.assertFalse(str(MINUS_ZERO)==str(PLUS_ZERO))
        s=map_type()
        for i in range(1,2000):
         s[i] = i
        self.assertFalse(MINUS_ZERO in s)
        self.assertFalse(PLUS_ZERO in s)
        s[MINUS_ZERO]=10
        self.assertTrue(MINUS_ZERO in s)
        self.assertTrue(PLUS_ZERO in s)


    def test_signed_zero2(self, map_type):
        MINUS_ZERO=float("-0.0")
        PLUS_ZERO =float("0.0")
        s=map_type()
        for i in range(1,2000):
         s[i] = i
        self.assertFalse(MINUS_ZERO in s)
        self.assertFalse(PLUS_ZERO in s)
        s[PLUS_ZERO] = 12
        self.assertTrue(MINUS_ZERO in s)
        self.assertTrue(PLUS_ZERO in s)
