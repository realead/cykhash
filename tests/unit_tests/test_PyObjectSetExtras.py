import sys

from unittestmock import UnitTestMock

from cykhash import PyObjectSet

class TestRefCounter(UnitTestMock): 

   def test_set_add_discard_right_refcnts(self):
      a=4200
      s=PyObjectSet()
      old_ref_cnt = sys.getrefcount(a)
      s.add(a)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+1, msg="first add")
      s.add(a) # shouldn't do anything
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+1, msg="second add")
      s.discard(a)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt, msg="discard")

   def test_set_deallocate_decrefs(self):
      a=4200
      s=PyObjectSet()
      old_ref_cnt = sys.getrefcount(a)
      s.add(a)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+1)
      del s
      self.assertEqual(sys.getrefcount(a), old_ref_cnt)

   def test_set_interator_right_refcnts(self):
      a=4200
      s=PyObjectSet()
      old_ref_cnt = sys.getrefcount(a)
      s.add(a)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+1)
      lst = list(s)
      # now also lst helds a additional reference
      self.assertEqual(sys.getrefcount(a), old_ref_cnt+2)

   def test_first_object_kept(self):
      a,b =float("nan"), float("nan")
      self.assertTrue(a is not b) #prerequisite
      s=PyObjectSet()
      s.add(a)
      s.add(b)
      lst = list(s)
      self.assertEqual(len(lst), 1)
      self.assertTrue(a is lst[0])

   def test_discard_with_equivalent_object(self):
      a,b =float("nan"), float("nan")
      self.assertTrue(a is not b) #prerequisite
      old_ref_cnt_a = sys.getrefcount(a)
      old_ref_cnt_b = sys.getrefcount(b)
      s=PyObjectSet()
      s.add(a)
      s.add(b)
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

      s.add(b)
      self.assertEqual(sys.getrefcount(a), old_ref_cnt_a)
      self.assertEqual(sys.getrefcount(b), old_ref_cnt_b+1)

      

