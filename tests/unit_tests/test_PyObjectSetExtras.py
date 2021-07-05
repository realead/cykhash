import sys

from unittestmock import UnitTestMock

from cykhash.compat import PYPY, assert_if_not_on_PYPY
import pytest
not_on_pypy = pytest.mark.skipif(PYPY, reason="pypy has no refcounting")

from cykhash import PyObjectSet

@not_on_pypy
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


def test_nan_float():
    nan1 = float("nan")
    nan2 = float("nan")
    assert_if_not_on_PYPY(nan1 is not nan2, reason="nan is singelton in PyPy")
    s = PyObjectSet()
    s.add(nan1)
    assert nan2 in s


def test_nan_complex():
    nan1 = complex(0, float("nan"))
    nan2 = complex(0, float("nan"))
    assert_if_not_on_PYPY(nan1 is not nan2, reason="nan is singelton in PyPy")
    s = PyObjectSet()
    s.add(nan1)
    assert nan2 in s


def test_nan_in_tuple():
    nan1 = (float("nan"),)
    nan2 = (float("nan"),)
    assert_if_not_on_PYPY(nan1[0] is not nan2[0], reason="nan is singelton in PyPy")
    s = PyObjectSet()
    s.add(nan1)
    assert nan2 in s


def test_nan_in_nested_tuple():
    nan1 = (1, (2, (float("nan"),)))
    nan2 = (1, (2, (float("nan"),)))
    other = (1, 2)
    s = PyObjectSet()
    s.add(nan1)
    assert nan2 in s
    assert other not in s


def test_unique_for_nan_objects_floats():
    s = PyObjectSet([float("nan") for i in range(50)])
    assert len(s) == 1


def test_unique_for_nan_objects_complex():
    s = PyObjectSet([complex(float("nan"), 1.0) for i in range(50)])
    assert len(s) == 1


def test_unique_for_nan_objects_tuple():
    s = PyObjectSet([(1.0, (float("nan"), 1.0)) for i in range(50)])
    assert len(s) == 1


def test_float_complex_int_are_equal_as_objects():
    s = PyObjectSet(range(129))
    assert 5 in s
    assert 5.0 in s
    assert 5.0+0j in s     

