import unittest
import uttemplate
import struct

from cykhash import Int64toInt64Map, Int32toInt32Map, Float64toInt64Map, Float32toInt32Map, PyObjectMap
from cykhash import Int64toFloat64Map, Int32toFloat32Map, Float64toFloat64Map, Float32toFloat32Map

@uttemplate.from_templates([Int64toInt64Map, Int32toInt32Map, Float64toInt64Map, Float32toInt32Map,
                            Int64toFloat64Map, Int32toFloat32Map, Float64toFloat64Map, Float32toFloat32Map,])
class CommonMapTester(unittest.TestCase): 

   def template_created_empty(self, map_type):
      s=map_type()
      self.assertEqual(len(s), 0)

   def template_put_int_once(self, map_type):
      s=map_type()
      s[1] = 43
      self.assertEqual(len(s), 1)
      self.assertEqual(s[1], 43)

   def template_put_int_twice(self, map_type):
      s=map_type()
      s[1] = 43
      s[1] = 43
      self.assertEqual(len(s), 1)
      self.assertEqual(s[1], 43)

   def template_add_two(self, map_type):
      s=map_type()
      s[1] = 43
      s[2] = 44
      self.assertEqual(len(s), 2)
      self.assertEqual(s[1], 43)
      self.assertEqual(s[2], 44)

   def template_add_many_twice(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       s[i] = 44
       self.assertEqual(len(s), i+1)
     #no changes for the second insert:
     for i in range(N):
       s[i] = 44
       self.assertEqual(len(s), N)


   def template_contains_none(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       self.assertFalse(i in s)


   def template_contains_all(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       s[i] = i+1
     for i in range(N):
       self.assertTrue(i in s)

   def template_contains_odd(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       if i%2==1:
        s[i] = i+1
     for i in range(N):
       self.assertEqual(i in s, i%2==1)

   def template_contains_even(self, map_type):
     N=1000
     s=map_type()
     for i in range(N):
       if i%2==0:
        s[i] = i+1
     for i in range(N):
       self.assertEqual(i in s, i%2==0)


   def template_delete_even(self, map_type):
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

   def template_negative_hint(self, map_type):
      with self.assertRaises(OverflowError) as context:
            map_type(number_of_elements_hint=-1)
      self.assertEqual("can't convert negative value to uint32_t", context.exception.args[0])

   def template_no_such_key(self, map_type):
      with self.assertRaises(KeyError) as context:
            map_type(number_of_elements_hint=100)[55]
      self.assertEqual(context.exception.args[0], 55)

   def template_zero_hint_ok(self, map_type):
      s = map_type(number_of_elements_hint=0)
      s[4] = 7
      s[5] = 7
      self.assertTrue(4 in s)
      self.assertTrue(5 in s)


   def template_as_int64_a_float(self, map_type):
      s = map_type(number_of_elements_hint=20, for_int=True)
      s[4] = 5.4
      self.assertEqual(s[4], 5)

   def template_as_int64_put_get(self, map_type):
      s = map_type(number_of_elements_hint=20, for_int=True)
      s[4] = 5
      self.assertEqual(s[4], 5)

   def template_as_float64_put_get(self, map_type):
      s = map_type(number_of_elements_hint=20, for_int=False)
      s[4] = 5
      self.assertEqual(s[4], 5)

###### special testers

@uttemplate.from_templates([Int64toInt64Map, Float64toInt64Map])
class Map64Tester(unittest.TestCase): 
   def template_put_get_int(self, map_type):
      s = map_type()
      s.put_int64(1, 43)
      self.assertEqual(len(s), 1)
      self.assertEqual(s.get_int64(1), 43)

   def template_int_to_float_to_int(self, map_type):
      s = map_type()
      s.put_int64(4, 7)
      s.put_float64(5, s.get_float64(4))
      self.assertTrue(s.get_int64(4), 7)

   def template_same_key_float_int(self, map_type):
      s = map_type()
      s.put_int64(4, 7)
      s.put_float64(4, 0.5)
      self.assertTrue(s.get_float64(4), 0.5)

@uttemplate.from_templates([Int32toInt32Map, Float32toInt32Map])
class Int32MapTester(unittest.TestCase): 
   def template_put_get_int(self, map_type):
      s = map_type()
      s.put_int32(1, 43)
      self.assertEqual(len(s), 1)
      self.assertEqual(s.get_int32(1), 43)

   def template_int_to_float_to_int(self, map_type):
      s = map_type()
      s.put_int32(4, 7)
      s.put_float32(5, s.get_float32(4))
      self.assertTrue(s.get_int32(4), 7)

   def template_same_key_float_int(self, map_type):
      s = map_type()
      s.put_int32(4, 7)
      s.put_float32(4, 0.5)
      self.assertTrue(s.get_float32(4), 0.5)


@uttemplate.from_templates([Float64toFloat64Map, Float32toFloat32Map, Float64toInt64Map, Float32toInt32Map, PyObjectMap])
class FloatTester(unittest.TestCase): 
    def template_nan_right(self, set_type):
        NAN=float("nan")
        s=set_type()
        self.assertFalse(NAN in s)
        s[NAN] = 1
        self.assertTrue(NAN in s)

    def template_all_nans_the_same(self, map_type):
        NAN1=struct.unpack("d", struct.pack("=Q", 9221120237041090560))[0]
        NAN2=struct.unpack("d", struct.pack("=Q", 9221120237061090562))[0]
        NAN3=struct.unpack("d", struct.pack("=Q", 9221120237042090562))[0]
        s=map_type()
        s[NAN1]=1
        s[NAN2]=1
        s[NAN3]=1
        for nan_id in range(9221120237041090560, 9221120237061090562, 1111):
            nan = struct.unpack("d", struct.pack("=Q", nan_id))[0]
            s[nan] = 1
        self.assertEqual(len(s), 1)
        for nan in range(2143299343, 2143499343):
            nan = struct.unpack("d", struct.pack("=Q", nan_id))[0]
            s[nan] = 1

    def test_all_nans_the_same_float32(self):
        s=Float32toInt32Map()
        for nan_id in range(2143299343, 2143499343):
            nan = struct.unpack("f", struct.pack("=I", nan_id))[0]
            s[nan] = 1
        self.assertEqual(len(s), 1)
        for nan_id in range(2143299343, 2143499343):
            nan = struct.unpack("f", struct.pack("=I", nan_id))[0]
            s[nan] = 1
 
#+0.0/-0.0 will break when there are more than 2**32 elements in the map
# bacause then hash-function will put them in different buckets 

    def template_signed_zero1(self, set_type):
        MINUS_ZERO=float("-0.0")
        PLUS_ZERO =float("0.0")
        self.assertFalse(str(MINUS_ZERO)==str(PLUS_ZERO))
        s=set_type()
        for i in range(1,2000):
         s[i] = i
        self.assertFalse(MINUS_ZERO in s)
        self.assertFalse(PLUS_ZERO in s)
        s[MINUS_ZERO]=10
        self.assertTrue(MINUS_ZERO in s)
        self.assertTrue(PLUS_ZERO in s)


    def template_signed_zero2(self, set_type):
        MINUS_ZERO=float("-0.0")
        PLUS_ZERO =float("0.0")
        s=set_type()
        for i in range(1,2000):
         s[i] = i
        self.assertFalse(MINUS_ZERO in s)
        self.assertFalse(PLUS_ZERO in s)
        s[PLUS_ZERO] = 12
        self.assertTrue(MINUS_ZERO in s)
        self.assertTrue(PLUS_ZERO in s)
