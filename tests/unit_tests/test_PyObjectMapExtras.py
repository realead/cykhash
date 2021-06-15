import sys
from unittestmock import UnitTestMock

from cykhash import PyObjectMap

class TestPyObjectMapMisc(UnitTestMock): 

   def test_from_keys_works(self):
      s=PyObjectMap.fromkeys(["a", "b", "c"], "kkk")
      self.assertEqual(len(s), 3)
      self.assertEqual(s["a"],"kkk") 


class TestRefCounterPyObjectMap(UnitTestMock): 

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


def test_nan_float():
    nan1 = float("nan")
    nan2 = float("nan")
    assert nan1 is not nan2
    table = PyObjectMap()
    table[nan1] =  42
    assert table[nan2] == 42


def test_nan_complex():
    nan1 = complex(0, float("nan"))
    nan2 = complex(0, float("nan"))
    assert nan1 is not nan2
    table = PyObjectMap()
    table[nan1] =  42
    assert table[nan2] == 42


def test_nan_in_tuple():
    nan1 = (float("nan"),)
    nan2 = (float("nan"),)
    assert nan1[0] is not nan2[0]
    table = PyObjectMap()
    table[nan1] =  42
    assert table[nan2] == 42


def test_nan_in_nested_tuple():
    nan1 = (1, (2, (float("nan"),)))
    nan2 = (1, (2, (float("nan"),)))
    other = (1, 2)
    table = PyObjectMap()
    table[nan1] =  42
    assert table[nan2] == 42
    assert other not in table


def test_unique_for_nan_objects_floats():
    table = PyObjectMap(zip([float("nan") for i in range(50)], range(50)))
    assert len(table) == 1


def test_unique_for_nan_objects_complex():
    table = PyObjectMap(zip([complex(float("nan"), 1.0) for i in range(50)], range(50)))
    assert len(table) == 1


def test_unique_for_nan_objects_tuple():
    table = PyObjectMap(zip([(1.0, (float("nan"), 1.0)) for i in range(50)], range(50)))
    assert len(table) == 1


def test_float_complex_int_are_equal_as_objects():
    table = PyObjectMap(zip(range(129), range(129)))
    assert table[5] == 5
    assert table[5.0] == 5
    assert table[5.0+0j] == 5


