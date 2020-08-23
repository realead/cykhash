import unittest
import uttemplate
import numpy as np

from cykhash import all_int64, all_int64_from_iter, Int64Set_from, Int64Set_from_buffer
from cykhash import all_int32, all_int32_from_iter, Int32Set_from, Int32Set_from_buffer
from cykhash import all_float64, all_float64_from_iter, Float64Set_from, Float64Set_from_buffer
from cykhash import all_float32, all_float32_from_iter, Float32Set_from, Float32Set_from_buffer
from cykhash import all_pyobject, all_pyobject_from_iter,  PyObjectSet_from, PyObjectSet_from_buffer

ALL={'int32': all_int32, 'int64': all_int64, 'float64' : all_float64, 'float32' : all_float32}
ALL_FROM_ITER={'int32': all_int32_from_iter, 'int64': all_int64_from_iter, 'float64' : all_float64_from_iter, 'float32' : all_float32_from_iter}
FROM_SET={'int32': Int32Set_from, 'int64': Int64Set_from, 'float64' : Float64Set_from, 'float32' : Float32Set_from, 'pyobject' : PyObjectSet_from}
BUFFER_SIZE = {'int32': 'i', 'int64': 'q', 'float64' : 'd', 'float32' : 'f'}


import array
@uttemplate.from_templates(['int64', 'int32', 'float64', 'float32'])
class AllTester(unittest.TestCase): 
    def template_all_yes(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], [2,4,6]*6)
        result=ALL[value_type](a,s)
        self.assertEqual(result, True)

    def template_all_yes_from_iter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=[2,4,6]*6
        result=ALL_FROM_ITER[value_type](a,s)
        self.assertEqual(result, True)

    def template_all_last_no(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], [2]*6+[3])
        result=ALL[value_type](a,s)
        self.assertEqual(result, False)

    def template_all_last_no_from_iter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=[2]*6+[3]
        result=ALL_FROM_ITER[value_type](a,s)
        self.assertEqual(result, False)

    def template_all_empty(self, value_type):
        s=FROM_SET[value_type]([])
        a=array.array(BUFFER_SIZE[value_type],[])
        result=ALL[value_type](a,s)
        self.assertEqual(result, True)

    def template_all_empty_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=[]
        result=ALL_FROM_ITER[value_type](a,s)
        self.assertEqual(result, True)

    def template_all_empty_set(self, value_type):
        s=FROM_SET[value_type]([])
        a=array.array(BUFFER_SIZE[value_type],[1])
        result=ALL[value_type](a,s)
        self.assertEqual(result, False)

    def template_all_empty_set_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=[1]
        result=ALL_FROM_ITER[value_type](a,s)
        self.assertEqual(result, False)


class AllTesterPyObject(unittest.TestCase): 
    def test_all_yes(self):
        s=PyObjectSet_from([2,4,666])
        a=np.array([2,4,666]*6, dtype=np.object)
        result=all_pyobject(a,s)
        self.assertEqual(result, True)

    def test_all_from_iter(self):
        s=PyObjectSet_from([2,4,666])
        a=[2,4,666]*6
        result=all_pyobject_from_iter(a,s)
        self.assertEqual(result, True)

    def test_all_last_no(self):
        s=PyObjectSet_from([2,4,666])
        a=np.array([2,4,666]*6+[3], dtype=np.object)
        result=all_pyobject(a,s)
        self.assertEqual(result, False)

    def test_all_last_no_from_iter(self):
        s=PyObjectSet_from([2,4,666])
        a=[2,4,666]*6+[3]
        result=all_pyobject_from_iter(a,s)
        self.assertEqual(result, False)

    def test_all_empty(self):
        s=PyObjectSet_from([])
        a=np.array([], dtype=np.object)
        result=all_pyobject(a,s)
        self.assertEqual(result, True)

    def test_all_empty_from_iter(self):
        s=PyObjectSet_from([])
        a=[]
        result=all_pyobject_from_iter(a,s)
        self.assertEqual(result, True)

    def test_all_empty_set(self):
        s=PyObjectSet_from([])
        a=np.array([1], dtype=np.object)
        result=all_pyobject(a,s)
        self.assertEqual(result, False)

    def test_all_empty_set_from_iter(self):
        s=PyObjectSet_from([])
        a=[1]
        result=all_pyobject_from_iter(a,s)
        self.assertEqual(result, False)

 
