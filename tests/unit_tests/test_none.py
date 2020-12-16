import pytest
from unittestmock import UnitTestMock

import numpy as np

from cykhash import none_int64, none_int64_from_iter, Int64Set_from, Int64Set_from_buffer
from cykhash import none_int32, none_int32_from_iter, Int32Set_from, Int32Set_from_buffer
from cykhash import none_float64, none_float64_from_iter, Float64Set_from, Float64Set_from_buffer
from cykhash import none_float32, none_float32_from_iter, Float32Set_from, Float32Set_from_buffer
from cykhash import none_pyobject, none_pyobject_from_iter,  PyObjectSet_from, PyObjectSet_from_buffer

NONE={'int32': none_int32, 'int64': none_int64, 'float64' : none_float64, 'float32' : none_float32}
NONE_FROM_ITER={'int32': none_int32_from_iter, 'int64': none_int64_from_iter, 'float64' : none_float64_from_iter, 'float32' : none_float32_from_iter}
FROM_SET={'int32': Int32Set_from, 'int64': Int64Set_from, 'float64' : Float64Set_from, 'float32' : Float32Set_from, 'pyobject' : PyObjectSet_from}
BUFFER_SIZE = {'int32': 'i', 'int64': 'q', 'float64' : 'd', 'float32' : 'f'}


import array

@pytest.mark.parametrize(
    "value_type",
    ['int64', 'int32', 'float64', 'float32']
)
class TestNone(UnitTestMock): 
    def test_none_yes(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], [1,3,5]*6)
        result=NONE[value_type](a,s)
        self.assertEqual(result, True)

    def test_none_yes_from_iter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=[1,3,5]*6
        result=NONE_FROM_ITER[value_type](a,s)
        self.assertEqual(result, True)

    def test_none_last_no(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], [1]*6+[2])
        result=NONE[value_type](a,s)
        self.assertEqual(result, False)

    def test_none_last_no_from_iter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=[1]*6+[2]
        result=NONE_FROM_ITER[value_type](a,s)
        self.assertEqual(result, False)

    def test_none_empty(self, value_type):
        s=FROM_SET[value_type]([])
        a=array.array(BUFFER_SIZE[value_type],[])
        result=NONE[value_type](a,s)
        self.assertEqual(result, True)

    def test_none_empty_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=[]
        result=NONE_FROM_ITER[value_type](a,s)
        self.assertEqual(result, True)

    def test_none_empty_set(self, value_type):
        s=FROM_SET[value_type]([])
        a=array.array(BUFFER_SIZE[value_type],[1])
        result=NONE[value_type](a,s)
        self.assertEqual(result, True)

    def test_none_empty_set_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=[1]
        result=NONE_FROM_ITER[value_type](a,s)
        self.assertEqual(result, True)

    def test_noniter_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=1
        with pytest.raises(TypeError) as context:
            NONE_FROM_ITER[value_type](a,s)
        self.assertTrue("object is not iterable" in str(context.value))

    def test_memview_none(self, value_type):
        s=FROM_SET[value_type]([])
        self.assertEqual(NONE[value_type](None,s), True)

    def test_dbnone(self, value_type):
        a=array.array(BUFFER_SIZE[value_type],[1])
        self.assertEqual(NONE[value_type](a,None), True)

    def test_dbnone_from_iter(self, value_type):
        a=1
        self.assertEqual(NONE_FROM_ITER[value_type](a,None), True)


class TestNonePyObject(UnitTestMock): 
    def test_none_yes(self):
        s=PyObjectSet_from([2,4,666])
        a=np.array([1,3,333]*6, dtype=np.object)
        result=none_pyobject(a,s)
        self.assertEqual(result, True)

    def test_none_from_iter(self):
        s=PyObjectSet_from([2,4,666])
        a=[1,3,333]*6
        result=none_pyobject_from_iter(a,s)
        self.assertEqual(result, True)

    def test_none_last_no(self):
        s=PyObjectSet_from([2,4,666])
        a=np.array([1,3,333]*6+[2], dtype=np.object)
        result=none_pyobject(a,s)
        self.assertEqual(result, False)

    def test_none_last_no_from_iter(self):
        s=PyObjectSet_from([2,4,666])
        a=[1,3,333]*6+[2]
        result=none_pyobject_from_iter(a,s)
        self.assertEqual(result, False)

    def test_none_empty(self):
        s=PyObjectSet_from([])
        a=np.array([], dtype=np.object)
        result=none_pyobject(a,s)
        self.assertEqual(result, True)

    def test_none_empty_from_iter(self):
        s=PyObjectSet_from([])
        a=[]
        result=none_pyobject_from_iter(a,s)
        self.assertEqual(result, True)

    def test_none_empty_set(self):
        s=PyObjectSet_from([])
        a=np.array([1], dtype=np.object)
        result=none_pyobject(a,s)
        self.assertEqual(result, True)

    def test_none_empty_set_from_iter(self):
        s=PyObjectSet_from([])
        a=[1]
        result=none_pyobject_from_iter(a,s)
        self.assertEqual(result, True)

    def test_noniter_from_iter(self):
        s=PyObjectSet_from([])
        a=1
        with pytest.raises(TypeError) as context:
            none_pyobject_from_iter(a,s)
        self.assertTrue("object is not iterable" in str(context.value))

    def test_memview_none(self):
        s=PyObjectSet_from([])
        self.assertEqual(none_pyobject(None,s), True)

    def test_dbnone(self):
        a=np.array([1], dtype=np.object)
        self.assertEqual(none_pyobject(a,None), True)

    def test_dbnone_from_iter(self):
        a=1
        self.assertEqual(none_pyobject_from_iter(a,None), True)

 
