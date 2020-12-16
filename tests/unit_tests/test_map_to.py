from unittestmock import UnitTestMock
import pytest

import numpy as np


from cykhash import Int64toInt64Map_to, Int64toInt64Map_from_buffers
from cykhash import Int64toFloat64Map_to, Int64toFloat64Map_from_buffers
from cykhash import Float64toInt64Map_to, Float64toInt64Map_from_buffers
from cykhash import Float64toFloat64Map_to, Float64toFloat64Map_from_buffers
from cykhash import Int32toInt32Map_to, Int32toInt32Map_from_buffers
from cykhash import Int32toFloat32Map_to, Int32toFloat32Map_from_buffers
from cykhash import Float32toInt32Map_to, Float32toInt32Map_from_buffers
from cykhash import Float32toFloat32Map_to, Float32toFloat32Map_from_buffers
from cykhash import PyObjectMap_to, PyObjectMap_from_buffers


MAP_TO_INT            = {'int32': Int32toInt32Map_to, 'int64': Int64toInt64Map_to, 'float64' : Float64toInt64Map_to, 'float32' : Float32toInt32Map_to}
MAP_TO_FLOAT          = {'int32': Int32toFloat32Map_to, 'int64': Int64toFloat64Map_to, 'float64' : Float64toFloat64Map_to, 'float32' : Float32toFloat32Map_to}
CREATOR_FROM_INT      = {'int32': Int32toInt32Map_from_buffers, 'int64': Int64toInt64Map_from_buffers, 'float64' : Float64toInt64Map_from_buffers, 'float32' : Float32toInt32Map_from_buffers}
CREATOR_FROM_FLOAT    = {'int32': Int32toFloat32Map_from_buffers, 'int64': Int64toFloat64Map_from_buffers, 'float64' : Float64toFloat64Map_from_buffers, 'float32' : Float32toFloat32Map_from_buffers}

DTYPE        =  {'int32': np.int32, 'int64': np.int64, 'float64' : np.float64, 'float32' : np.float32}
INT_DTYPE    =  {'int32': np.int32, 'int64': np.int64, 'float64' : np.int64, 'float32' : np.int32}
FLOAT_DTYPE  =  {'int32': np.float32, 'int64': np.float64, 'float64' : np.float64, 'float32' : np.float32}


@pytest.mark.parametrize(
    "value_type",
    ['int64', 'int32', 'float64', 'float32']
)
class TestMapTo(UnitTestMock): 
    def test_None_map(self, value_type):
        k=np.array([]).astype(DTYPE[value_type])
        ints=np.array([]).astype(INT_DTYPE[value_type])
        floats=np.array([]).astype(FLOAT_DTYPE[value_type])
        with pytest.raises(TypeError) as context:
            MAP_TO_INT[value_type](None,k,ints)
        self.assertTrue("'NoneType' is not a map" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            MAP_TO_FLOAT[value_type](None,k,floats)
        self.assertTrue("'NoneType' is not a map" in context.value.args[0])

    def test_different_lengths_ints(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        ints=np.array(range(0,2*N,2)).astype(INT_DTYPE[value_type])
        mymap = CREATOR_FROM_INT[value_type](keys, ints)
        results=np.zeros(N+1).astype(INT_DTYPE[value_type])
        with pytest.raises(ValueError) as context:
            MAP_TO_INT[value_type](mymap, keys, results)
        self.assertTrue("Different lengths" in context.value.args[0])

    def test_different_lengths_floats(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        floats=np.array(range(0,2*N,2)).astype(FLOAT_DTYPE[value_type])
        mymap = CREATOR_FROM_FLOAT[value_type](keys, floats)
        results=np.zeros(N+1).astype(FLOAT_DTYPE[value_type])
        with pytest.raises(ValueError) as context:
            MAP_TO_FLOAT[value_type](mymap, keys, results)
        self.assertTrue("Different lengths" in context.value.args[0])

    def test_map_to_int_simple(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        vals=np.array(range(0,2*N,2)).astype(INT_DTYPE[value_type])
        mymap = CREATOR_FROM_INT[value_type](keys, vals)
        result = np.zeros_like(vals)
        self.assertEqual(MAP_TO_INT[value_type](mymap, keys, result), N)
        self.assertTrue(np.array_equal(vals, result))

    def test_map_to_float_simple(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        vals=np.array(range(0,2*N,2)).astype(FLOAT_DTYPE[value_type])
        mymap = CREATOR_FROM_FLOAT[value_type](keys, vals)
        result = np.zeros_like(vals)
        self.assertEqual(MAP_TO_FLOAT[value_type](mymap, keys, result), N)
        self.assertTrue(np.array_equal(vals, result))

    def test_map_with_stop_int(self, value_type):
        keys=np.arange(3).astype(DTYPE[value_type])
        vals=np.array([5,6,7]).astype(INT_DTYPE[value_type])
        mymap = CREATOR_FROM_INT[value_type](keys, vals)
        query = np.array([2,55,1]).astype(DTYPE[value_type])
        result = np.zeros(query.shape, dtype=INT_DTYPE[value_type])
        self.assertEqual(MAP_TO_INT[value_type](mymap, query, result), 1)
        self.assertEqual(result[0], vals[-1])

    def test_map_with_stop_float(self, value_type):
        keys=np.arange(3).astype(DTYPE[value_type])
        vals=np.array([5,6,7]).astype(FLOAT_DTYPE[value_type])
        mymap = CREATOR_FROM_FLOAT[value_type](keys, vals)
        query = np.array([2,55,1]).astype(DTYPE[value_type])
        result = np.zeros(query.shape, dtype=FLOAT_DTYPE[value_type])
        self.assertEqual(MAP_TO_FLOAT[value_type](mymap, query, result), 1)
        self.assertEqual(result[0], vals[-1])

    def test_map_no_stop_int(self, value_type):
        keys=np.arange(3).astype(DTYPE[value_type])
        vals=np.array([5,6,7]).astype(INT_DTYPE[value_type])
        mymap = CREATOR_FROM_INT[value_type](keys, vals)
        query = np.array([2,55,1,66,0]).astype(DTYPE[value_type])
        result = np.zeros(query.shape, dtype=INT_DTYPE[value_type])
        expected = np.array([7,42,6,42,5]).astype(INT_DTYPE[value_type])
        self.assertEqual(MAP_TO_INT[value_type](mymap, query, result, False, 42), 3)
        self.assertTrue(np.array_equal(expected, result))

    def test_map_no_stop_float(self, value_type):
        keys=np.arange(3).astype(DTYPE[value_type])
        vals=np.array([5,6,7]).astype(FLOAT_DTYPE[value_type])
        mymap = CREATOR_FROM_FLOAT[value_type](keys, vals)
        query = np.array([2,55,1,66,0]).astype(DTYPE[value_type])
        result = np.zeros(query.shape, dtype=FLOAT_DTYPE[value_type])
        expected = np.array([7,42,6,42,5]).astype(FLOAT_DTYPE[value_type])
        self.assertEqual(MAP_TO_FLOAT[value_type](mymap, query, result, False, 42), 3)
        self.assertTrue(np.array_equal(expected, result))


class TestMapToPyObject(UnitTestMock): 
    def test_None_map(self):
        objs=np.array([]).astype(np.object)
        with pytest.raises(TypeError) as context:
           PyObjectMap_to(None,objs,objs)
        self.assertTrue("'NoneType' is not a map" in context.value.args[0])

    def test_different_lengths(self):
        N = 1000
        keys=np.arange(N).astype(np.object)
        mymap = PyObjectMap_from_buffers(keys, keys)
        results=np.zeros(N+1).astype(np.object)
        with pytest.raises(ValueError) as context:
            PyObjectMap_to(mymap, keys, results)
        self.assertTrue("Different lengths" in context.value.args[0])

    def test_map_to_simple(self):
        N = 1000
        keys=np.arange(N).astype(np.object)
        vals=np.array(range(0,2*N,2)).astype(np.object)
        mymap = PyObjectMap_from_buffers(keys, vals)
        result = np.zeros_like(vals)
        self.assertEqual(PyObjectMap_to(mymap, keys, result), N)
        self.assertTrue(np.array_equal(vals,result))

    def test_map_with_stop(self):
        keys=np.arange(3).astype(np.object)
        vals=np.array([5,6,7]).astype(np.object)
        mymap = PyObjectMap_from_buffers(keys, vals)
        query = np.array([2,55,1]).astype(np.object)
        result = np.zeros_like(query)
        self.assertEqual(PyObjectMap_to(mymap, query, result), 1)
        self.assertEqual(result[0], vals[-1])

    def test_map_no_stop_float(self):
        keys=np.arange(3).astype(np.object)
        vals=np.array([5,6,7]).astype(np.object)
        mymap = PyObjectMap_from_buffers(keys, vals)
        query = np.array([2,55,1,66,0]).astype(np.object)
        result = np.zeros_like(query)
        expected = np.array([7,42,6,42,5]).astype(np.object)
        self.assertEqual(PyObjectMap_to(mymap, query, result, False, 42), 3)
        self.assertTrue(np.array_equal(expected, result))
