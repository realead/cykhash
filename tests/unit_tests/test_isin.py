import pytest
from unittestmock import UnitTestMock

import numpy as np

from cykhash import isin_int64, Int64Set_from, Int64Set_from_buffer
from cykhash import isin_int32, Int32Set_from, Int32Set_from_buffer
from cykhash import isin_float64, Float64Set_from, Float64Set_from_buffer
from cykhash import isin_float32, Float32Set_from, Float32Set_from_buffer
from cykhash import isin_pyobject,  PyObjectSet_from, PyObjectSet_from_buffer

ISIN={'int32': isin_int32, 'int64': isin_int64, 'float64' : isin_float64, 'float32' : isin_float32}
FROM_SET={'int32': Int32Set_from, 'int64': Int64Set_from, 'float64' : Float64Set_from, 'float32' : Float32Set_from, 'pyobject' : PyObjectSet_from}
BUFFER_SIZE = {'int32': 'i', 'int64': 'q', 'float64' : 'd', 'float32' : 'f'}
FROM_BUFFER_SET={'int32': Int32Set_from_buffer, 'int64': Int64Set_from_buffer, 'float64' : Float64Set_from_buffer, 'float32' : Float32Set_from_buffer, 'pyobject' : PyObjectSet_from_buffer}



@pytest.mark.parametrize(
    "value_type",
    ['int64', 'int32', 'float64', 'float32', 'pyobject']
)
class TestInt64Set_from(UnitTestMock):
    def test_create(self, value_type):
        lst=[6,7,8]
        s=FROM_SET[value_type](list(lst))
        self.assertEqual(len(s), len(lst))
        for x in lst:
            self.assertTrue(x in s)


import array
@pytest.mark.parametrize(
    "value_type",
    ['int64', 'int32', 'float64', 'float32']
)
class TestBuffer(UnitTestMock): 
    def test_isin(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], range(0,7))
        result=array.array('B', [False]*7)
        ISIN[value_type](a,s,result)
        expected=array.array('B', [False, False, True, False, True, False, True])
        self.assertTrue(expected==result)

    def test_isin_result_shorter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], range(0,7))
        result=array.array('B', [False]*6)
        with pytest.raises(ValueError) as context:
            ISIN[value_type](a,s,result)
        self.assertEqual("Different sizes for query(7) and result(6)", context.value.args[0])

    def test_isin_result_longer(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], range(0,7))
        result=array.array('B', [False]*8)
        with pytest.raises(ValueError) as context:
            ISIN[value_type](a,s,result)
        self.assertEqual("Different sizes for query(7) and result(8)", context.value.args[0])

    def test_isin_db_none(self, value_type):
        a=array.array(BUFFER_SIZE[value_type], range(0,7))
        result=array.array('B', [True]*7)
        ISIN[value_type](a,None,result)
        expected=array.array('B', [False, False, False, False, False, False, False])
        self.assertTrue(expected==result)

    def test_isin_nones(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        ISIN[value_type](None,s,None)
        self.assertTrue(True)

    def test_from_buffer(self, value_type):
        a=array.array(BUFFER_SIZE[value_type], [6,7,8])
        s=FROM_BUFFER_SET[value_type](a)
        self.assertEqual(len(s), len(a))
        for x in a:
            self.assertTrue(x in s)


class TestBufferPyObject(UnitTestMock): 
    def test_pyobject_isin(self):
        s=PyObjectSet_from([2,4,6])
        a=np.array(range(0,7), dtype=np.object)
        result=array.array('B', [False]*7)
        isin_pyobject(a,s,result)
        expected=array.array('B', [False, False, True, False, True, False, True])
        self.assertTrue(expected==result)

    def test_pyobject_from_buffer(self):
        a=np.array([6,7,8], dtype=np.object)
        s=PyObjectSet_from_buffer(a)
        self.assertEqual(len(s), len(a))
        for x in a:
            self.assertTrue(x in s)

    def test_isin_result_shorter(self):      
        s=PyObjectSet_from([2,4,6])
        a=np.array(range(0,7), dtype=np.object)
        result=array.array('B', [False]*6)
        with pytest.raises(ValueError) as context:
            isin_pyobject(a,s,result)
        self.assertEqual("Different sizes for query(7) and result(6)", context.value.args[0])

    def test_isin_result_longer(self):
        s=PyObjectSet_from([2,4,6])
        a=np.array(range(0,7), dtype=np.object)
        result=array.array('B', [False]*8)
        with pytest.raises(ValueError) as context:
            isin_pyobject(a,s,result)
        self.assertEqual("Different sizes for query(7) and result(8)", context.value.args[0])

    def test_isin_db_none(self):
        a=np.array(range(0,7), dtype=np.object)
        result=array.array('B', [True]*7)
        isin_pyobject(a,None,result)
        expected=array.array('B', [False, False, False, False, False, False, False])
        self.assertTrue(expected==result)

    def test_isin_nones(self):
        s=PyObjectSet_from([2,4,6])
        isin_pyobject(None,s,None)
        self.assertTrue(True)
 
