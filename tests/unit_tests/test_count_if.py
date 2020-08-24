import unittest
import uttemplate
import numpy as np

from cykhash import count_if_int64, count_if_int64_from_iter, Int64Set_from, Int64Set_from_buffer
from cykhash import count_if_int32, count_if_int32_from_iter, Int32Set_from, Int32Set_from_buffer
from cykhash import count_if_float64, count_if_float64_from_iter, Float64Set_from, Float64Set_from_buffer
from cykhash import count_if_float32, count_if_float32_from_iter, Float32Set_from, Float32Set_from_buffer
from cykhash import count_if_pyobject, count_if_pyobject_from_iter,  PyObjectSet_from, PyObjectSet_from_buffer

COUNT_IF={'int32': count_if_int32, 'int64': count_if_int64, 'float64' : count_if_float64, 'float32' : count_if_float32}
COUNT_IF_FROM_ITER={'int32': count_if_int32_from_iter, 'int64': count_if_int64_from_iter, 'float64' : count_if_float64_from_iter, 'float32' : count_if_float32_from_iter}
FROM_SET={'int32': Int32Set_from, 'int64': Int64Set_from, 'float64' : Float64Set_from, 'float32' : Float32Set_from, 'pyobject' : PyObjectSet_from}
BUFFER_SIZE = {'int32': 'i', 'int64': 'q', 'float64' : 'd', 'float32' : 'f'}


import array
@uttemplate.from_templates(['int64', 'int32', 'float64', 'float32'])
class CountIfTester(unittest.TestCase): 
    def template_count_if_all(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], [2,4,6]*6)
        result=COUNT_IF[value_type](a,s)
        self.assertEqual(result, 18)

    def template_count_if_all_from_iter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=[2,4,6]*6
        result=COUNT_IF_FROM_ITER[value_type](a,s)
        self.assertEqual(result, 18)

    def template_count_if_but_last(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], [2]*6+[1])
        result=COUNT_IF[value_type](a,s)
        self.assertEqual(result, 6)

    def template_count_if_but_last_from_iter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=[2]*6+[1]
        result=COUNT_IF_FROM_ITER[value_type](a,s)
        self.assertEqual(result, 6)

    def template_count_if_empty(self, value_type):
        s=FROM_SET[value_type]([])
        a=array.array(BUFFER_SIZE[value_type],[])
        result=COUNT_IF[value_type](a,s)
        self.assertEqual(result, 0)

    def template_count_if_empty_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=[]
        result=COUNT_IF_FROM_ITER[value_type](a,s)
        self.assertEqual(result, 0)

    def template_count_if_empty_set(self, value_type):
        s=FROM_SET[value_type]([])
        a=array.array(BUFFER_SIZE[value_type],[1])
        result=COUNT_IF[value_type](a,s)
        self.assertEqual(result, 0)

    def template_count_if_empty_set_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=[1]
        result=COUNT_IF_FROM_ITER[value_type](a,s)
        self.assertEqual(result, 0)

    def template_noniter_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=1
        with self.assertRaises(TypeError) as context:
            COUNT_IF_FROM_ITER[value_type](a,s)
        self.assertTrue("object is not iterable" in context.exception.args[0])


class CountIfTesterPyObject(unittest.TestCase): 
    def test_count_if_all(self):
        s=PyObjectSet_from([2,4,666])
        a=np.array([2,4,666]*6, dtype=np.object)
        result=count_if_pyobject(a,s)
        self.assertEqual(result, 18)

    def test_count_if_all_from_iter(self):
        s=PyObjectSet_from([2,4,666])
        a=[2,4,666]*6
        result=count_if_pyobject_from_iter(a,s)
        self.assertEqual(result, 18)

    def test_count_if_but_last(self):
        s=PyObjectSet_from([2,4,666])
        a=np.array([2,4,666]*6+[2, 1], dtype=np.object)
        result=count_if_pyobject(a,s)
        self.assertEqual(result, 19)

    def test_count_if_butlast_from_iter(self):
        s=PyObjectSet_from([2,4,666, "str"])
        a=[2,4,666,"str"]*6+[2,1]
        result=count_if_pyobject_from_iter(a,s)
        self.assertEqual(result, 25)

    def test_count_if_empty(self):
        s=PyObjectSet_from([])
        a=np.array([], dtype=np.object)
        result=count_if_pyobject(a,s)
        self.assertEqual(result, 0)

    def test_count_if_empty_from_iter(self):
        s=PyObjectSet_from([])
        a=[]
        result=count_if_pyobject_from_iter(a,s)
        self.assertEqual(result, 0)

    def test_count_if_empty_set(self):
        s=PyObjectSet_from([])
        a=np.array([1], dtype=np.object)
        result=count_if_pyobject(a,s)
        self.assertEqual(result, 0)

    def test_count_if_empty_set_from_iter(self):
        s=PyObjectSet_from([])
        a=[1]
        result=count_if_pyobject_from_iter(a,s)
        self.assertEqual(result, 0)

    def test_noniter_from_iter(self):
        s=PyObjectSet_from([])
        a=1
        with self.assertRaises(TypeError) as context:
            count_if_pyobject_from_iter(a,s)
        self.assertTrue("object is not iterable" in context.exception.args[0])

 
