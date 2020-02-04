import unittest
import uttemplate
import struct

from cykhash import Int64to64Map, Int32to32Map

@uttemplate.from_templates([Int64to64Map, Int32to32Map])
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
            map_type(-1)
      self.assertEqual("can't convert negative value to uint32_t", context.exception.args[0])

   def template_no_such_key(self, map_type):
      with self.assertRaises(KeyError) as context:
            map_type(100)[55]
      self.assertEqual("No such key: 55", context.exception.args[0])

   def template_zero_hint_ok(self, map_type):
      s = map_type(0)
      s[4] = 7
      s[5] = 7
      self.assertTrue(4 in s)
      self.assertTrue(5 in s)


   def template_as_int64_a_float(self, map_type):
      s = map_type(20, True)
      s[4] = 5.4
      self.assertEqual(s[4], 5)

   def template_as_int64_put_get(self, map_type):
      s = map_type(20, True)
      s[4] = 5
      self.assertEqual(s[4], 5)

   def template_as_float64_put_get(self, map_type):
      s = map_type(20, False)
      s[4] = 5
      self.assertEqual(s[4], 5)

###### special testers

class Int64MapTester(unittest.TestCase): 
   def test_put_get_int(self):
      s=Int64to64Map()
      s.put_int64(1, 43)
      self.assertEqual(len(s), 1)
      self.assertEqual(s.get_int64(1), 43)

   def test_int_to_float_to_int(self):
      s = Int64to64Map()
      s.put_int64(4, 7)
      s.put_float64(5, s.get_float64(4))
      self.assertTrue(s.get_int64(4), 7)

   def test_same_key_float_int(self):
      s = Int64to64Map()
      s.put_int64(4, 7)
      s.put_float64(4, 0.5)
      self.assertTrue(s.get_float64(4), 0.5)


class Int32MapTester(unittest.TestCase): 
   def test_put_get_int(self):
      s=Int32to32Map()
      s.put_int32(1, 43)
      self.assertEqual(len(s), 1)
      self.assertEqual(s.get_int32(1), 43)

   def test_int_to_float_to_int(self):
      s = Int32to32Map()
      s.put_int32(4, 7)
      s.put_float32(5, s.get_float32(4))
      self.assertTrue(s.get_int32(4), 7)

   def test_same_key_float_int(self):
      s = Int32to32Map()
      s.put_int32(4, 7)
      s.put_float32(4, 0.5)
      self.assertTrue(s.get_float32(4), 0.5)




