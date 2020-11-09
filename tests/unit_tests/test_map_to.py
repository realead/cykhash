import unittest
import uttemplate
import numpy as np


from cykhash import Int64to64Map_to_int64, Int64to64Map_to_float64, Int64to64Map_from_int64_buffer, Int64to64Map_from_float64_buffer
from cykhash import Float64to64Map_to_int64, Float64to64Map_to_float64, Float64to64Map_from_int64_buffer, Float64to64Map_from_float64_buffer
from cykhash import Int32to32Map_to_int32, Int32to32Map_to_float32, Int32to32Map_from_int32_buffer, Int32to32Map_from_float32_buffer
from cykhash import Float32to32Map_to_int32, Float32to32Map_to_float32, Float32to32Map_from_int32_buffer, Float32to32Map_from_float32_buffer
from cykhash import PyObjectMap_to_object, PyObjectMap_from_object_buffer


MAP_TO_INT            = {'int32': Int32to32Map_to_int32, 'int64': Int64to64Map_to_int64, 'float64' : Float64to64Map_to_int64, 'float32' : Float32to32Map_to_int32}
MAP_TO_FLOAT          = {'int32': Int32to32Map_to_float32, 'int64': Int64to64Map_to_float64, 'float64' : Float64to64Map_to_float64, 'float32' : Float32to32Map_to_float32}
CREATOR_FROM_INT      = {'int32': Int32to32Map_from_int32_buffer, 'int64': Int64to64Map_from_int64_buffer, 'float64' : Float64to64Map_from_int64_buffer, 'float32' : Float32to32Map_from_int32_buffer}
CREATOR_FROM_FLOAT    = {'int32': Int32to32Map_from_float32_buffer, 'int64': Int64to64Map_from_float64_buffer, 'float64' : Float64to64Map_from_float64_buffer, 'float32' : Float32to32Map_from_float32_buffer}

DTYPE        =  {'int32': np.int32, 'int64': np.int64, 'float64' : np.float64, 'float32' : np.float32}
INT_DTYPE    =  {'int32': np.int32, 'int64': np.int64, 'float64' : np.int64, 'float32' : np.int32}
FLOAT_DTYPE  =  {'int32': np.float32, 'int64': np.float64, 'float64' : np.float64, 'float32' : np.float32}


@uttemplate.from_templates(['int64', 'int32', 'float64', 'float32'])
class MapTester(unittest.TestCase): 
    def template_None_map(self, value_type):
        k=np.array([]).astype(DTYPE[value_type])
        ints=np.array([]).astype(INT_DTYPE[value_type])
        floats=np.array([]).astype(FLOAT_DTYPE[value_type])
        with self.assertRaises(TypeError) as context:
            MAP_TO_INT[value_type](None,k,ints)
        self.assertTrue("'NoneType' is not a map" in context.exception.args[0])
        with self.assertRaises(TypeError) as context:
            MAP_TO_FLOAT[value_type](None,k,floats)
        self.assertTrue("'NoneType' is not a map" in context.exception.args[0])

    def template_different_lengths_ints(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        ints=np.array(range(0,2*N,2)).astype(INT_DTYPE[value_type])
        mymap = CREATOR_FROM_INT[value_type](keys, ints)
        results=np.zeros(N+1).astype(INT_DTYPE[value_type])
        with self.assertRaises(ValueError) as context:
            MAP_TO_INT[value_type](mymap, keys, results)
        self.assertTrue("Different lengths" in context.exception.args[0])

    def template_different_lengths_floats(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        floats=np.array(range(0,2*N,2)).astype(FLOAT_DTYPE[value_type])
        mymap = CREATOR_FROM_FLOAT[value_type](keys, floats)
        results=np.zeros(N+1).astype(FLOAT_DTYPE[value_type])
        with self.assertRaises(ValueError) as context:
            MAP_TO_FLOAT[value_type](mymap, keys, results)
        self.assertTrue("Different lengths" in context.exception.args[0])

    def template_map_type_missmatch(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        vals_int=np.array(range(0,2*N,2)).astype(INT_DTYPE[value_type])
        vals_float=np.array(range(0,2*N,2)).astype(FLOAT_DTYPE[value_type])
        mymap_for_ints = CREATOR_FROM_INT[value_type](keys, vals_int)
        mymap_for_floats = CREATOR_FROM_FLOAT[value_type](keys, vals_float)
        with self.assertRaises(TypeError) as context:
            MAP_TO_FLOAT[value_type](mymap_for_ints, keys, vals_float)
        self.assertTrue("Map is not for floats" in context.exception.args[0])
        with self.assertRaises(TypeError) as context:
            MAP_TO_INT[value_type](mymap_for_floats, keys, vals_int)
        self.assertTrue("Map is not for ints" in context.exception.args[0])

    def template_map_to_int_simple(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        vals=np.array(range(0,2*N,2)).astype(INT_DTYPE[value_type])
        mymap = CREATOR_FROM_INT[value_type](keys, vals)
        result = np.zeros_like(vals)
        self.assertEqual(MAP_TO_INT[value_type](mymap, keys, result), N)
        self.assertTrue(np.array_equal(vals, result))

    def template_map_to_float_simple(self, value_type):
        N = 1000
        keys=np.arange(N).astype(DTYPE[value_type])
        vals=np.array(range(0,2*N,2)).astype(FLOAT_DTYPE[value_type])
        mymap = CREATOR_FROM_FLOAT[value_type](keys, vals)
        result = np.zeros_like(vals)
        self.assertEqual(MAP_TO_FLOAT[value_type](mymap, keys, result), N)
        self.assertTrue(np.array_equal(vals, result))

    def template_map_with_stop_int(self, value_type):
        keys=np.arange(3).astype(DTYPE[value_type])
        vals=np.array([5,6,7]).astype(INT_DTYPE[value_type])
        mymap = CREATOR_FROM_INT[value_type](keys, vals)
        query = np.array([2,55,1]).astype(DTYPE[value_type])
        result = np.zeros(query.shape, dtype=INT_DTYPE[value_type])
        self.assertEqual(MAP_TO_INT[value_type](mymap, query, result), 1)
        self.assertEqual(result[0], vals[-1])

    def template_map_with_stop_float(self, value_type):
        keys=np.arange(3).astype(DTYPE[value_type])
        vals=np.array([5,6,7]).astype(FLOAT_DTYPE[value_type])
        mymap = CREATOR_FROM_FLOAT[value_type](keys, vals)
        query = np.array([2,55,1]).astype(DTYPE[value_type])
        result = np.zeros(query.shape, dtype=FLOAT_DTYPE[value_type])
        self.assertEqual(MAP_TO_FLOAT[value_type](mymap, query, result), 1)
        self.assertEqual(result[0], vals[-1])

    def template_map_no_stop_int(self, value_type):
        keys=np.arange(3).astype(DTYPE[value_type])
        vals=np.array([5,6,7]).astype(INT_DTYPE[value_type])
        mymap = CREATOR_FROM_INT[value_type](keys, vals)
        query = np.array([2,55,1,66,0]).astype(DTYPE[value_type])
        result = np.zeros(query.shape, dtype=INT_DTYPE[value_type])
        expected = np.array([7,42,6,42,5]).astype(INT_DTYPE[value_type])
        self.assertEqual(MAP_TO_INT[value_type](mymap, query, result, False, 42), 3)
        self.assertTrue(np.array_equal(expected, result))

    def template_map_no_stop_float(self, value_type):
        keys=np.arange(3).astype(DTYPE[value_type])
        vals=np.array([5,6,7]).astype(FLOAT_DTYPE[value_type])
        mymap = CREATOR_FROM_FLOAT[value_type](keys, vals)
        query = np.array([2,55,1,66,0]).astype(DTYPE[value_type])
        result = np.zeros(query.shape, dtype=FLOAT_DTYPE[value_type])
        expected = np.array([7,42,6,42,5]).astype(FLOAT_DTYPE[value_type])
        self.assertEqual(MAP_TO_FLOAT[value_type](mymap, query, result, False, 42), 3)
        self.assertTrue(np.array_equal(expected, result))

class MapTesterPyObject(unittest.TestCase): 
    def test_None_map(self):
        objs=np.array([]).astype(np.object)
        with self.assertRaises(TypeError) as context:
           PyObjectMap_to_object(None,objs,objs)
        self.assertTrue("'NoneType' is not a map" in context.exception.args[0])

    def test_different_lengths(self):
        N = 1000
        keys=np.arange(N).astype(np.object)
        mymap = PyObjectMap_from_object_buffer(keys, keys)
        results=np.zeros(N+1).astype(np.object)
        with self.assertRaises(ValueError) as context:
            PyObjectMap_to_object(mymap, keys, results)
        self.assertTrue("Different lengths" in context.exception.args[0])

    def test_map_to_simple(self):
        N = 1000
        keys=np.arange(N).astype(np.object)
        vals=np.array(range(0,2*N,2)).astype(np.object)
        mymap = PyObjectMap_from_object_buffer(keys, vals)
        result = np.zeros_like(vals)
        self.assertEqual(PyObjectMap_to_object(mymap, keys, result), N)
        self.assertTrue(np.array_equal(vals,result))

    def template_map_with_stop(self):
        keys=np.arange(3).astype(np.object)
        vals=np.array([5,6,7]).astype(np.object)
        mymap = PyObjectMap_from_object_buffer(keys, vals)
        query = np.array([2,55,1]).astype(np.object)
        result = np.zeros_like(query)
        self.assertEqual(PyObjectMap_to_object(mymap, query, result), 1)
        self.assertEqual(result[0], vals[-1])

    def template_map_no_stop_float(self, value_type):
        keys=np.arange(3).astype(np.object)
        vals=np.array([5,6,7]).astype(np.object)
        mymap = PyObjectMap_from_object_buffer(keys, vals)
        query = np.array([2,55,1,66,0]).astype(np.object)
        result = np.zeros_like(query)
        expected = np.array([7,42,6,42,5]).astype(np.object)
        self.assertEqual(PyObjectMap_to_object(mymap, query, result, False, 42), 1)
        self.assertTrue(np.array_equal(expected, result))
