import sys
import unittest

from cykhash import PyObjectMap

class RefCounterTester(unittest.TestCase): 

   def test_map_put_discard_right_refcnts(self):
      a=4200
      s=PyObjectMap()
      old_ref_cnt = sys.getrefcount(a)
      s[a] = a
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+2, msg="first add")
      s[a] = a # shouldn't do anything
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+2, msg="second add")
      s.discard(a)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt, msg="discard")

   def test_map_deallocate_decrefs(self):
      a=4200
      s=PyObjectMap()
      old_ref_cnt = sys.getrefcount(a)
      s[a] = a
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+2)
      del s
      self.assertEqual(sys.getrefcount(a), old_ref_cnt)

   def test_map_interator_right_refcnts(self):
      a=4200
      s=PyObjectMap()
      old_ref_cnt = sys.getrefcount(a)
      s[a] = a
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+2)
      lst = list(s.items())
      # now also lst helds two additional references
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+4)

   def test_first_object_kept(self):
      a,b =float("nan"), float("nan")
      self.assertTrue(a is not b) #prerequisite
      s=PyObjectMap()
      s[a] = a
      s[b] = b
      lst = list(s.items())
      self.assertEqual(len(lst), 1)
      self.assertTrue(a is lst[0][0])

   def test_discard_with_equivalent_object(self):
      a,b =float("nan"), float("nan")
      self.assertTrue(a is not b) #prerequisite
      old_ref_cnt_a = sys.getrefcount(a)
      old_ref_cnt_b = sys.getrefcount(b)
      s=PyObjectMap()
      s[a] = None
      s[b] = None
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a+1)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b)
      
      self.assertTrue(b in s)
      self.assertTrue(a in s)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a+1)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b)

      s.discard(b)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b)

      s.discard(b)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b)

      s.discard(a)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b)

      s[b] = None
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b+1)

   def test_rewrite_works(self):
      a,b =float("nan"), float("nan")
      self.assertTrue(a is not b) #prerequisite
      old_ref_cnt_a = sys.getrefcount(a)
      old_ref_cnt_b = sys.getrefcount(b)
      s=PyObjectMap()
      s[a] = a
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a+2)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b)
      
      s[b] = b    
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a+1)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b+1)

      del s
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b)

      

