import unittest
import uttemplate
import numpy as np

from cykhash import any_int64, any_int64_from_iter, Int64Set_from, Int64Set_from_buffer
from cykhash import any_int32, any_int32_from_iter, Int32Set_from, Int32Set_from_buffer
from cykhash import any_float64, any_float64_from_iter, Float64Set_from, Float64Set_from_buffer
from cykhash import any_float32, any_float32_from_iter, Float32Set_from, Float32Set_from_buffer
from cykhash import any_pyobject, any_pyobject_from_iter,  PyObjectSet_from, PyObjectSet_from_buffer

ANY={'int32': any_int32, 'int64': any_int64, 'float64' : any_float64, 'float32' : any_float32}
ANY_FROM_ITER={'int32': any_int32_from_iter, 'int64': any_int64_from_iter, 'float64' : any_float64_from_iter, 'float32' : any_float32_from_iter}
FROM_SET={'int32': Int32Set_from, 'int64': Int64Set_from, 'float64' : Float64Set_from, 'float32' : Float32Set_from, 'pyobject' : PyObjectSet_from}
BUFFER_SIZE = {'int32': 'i', 'int64': 'q', 'float64' : 'd', 'float32' : 'f'}


import array
@uttemplate.from_templates(['int64', 'int32', 'float64', 'float32'])
class ANYTester(unittest.TestCase): 
    def template_any_no(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], [1,3,5]*6)
        result=ANY[value_type](a,s)
        self.assertEqual(result, False)

    def template_any_no_from_iter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=[1,3,5]*6
        result=ANY_FROM_ITER[value_type](a,s)
        self.assertEqual(result, False)

    def template_any_last_yes(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], [1]*6+[2])
        result=ANY[value_type](a,s)
        self.assertEqual(result, True)

    def template_any_last_yes_from_iter(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=[1]*6+[2]
        result=ANY_FROM_ITER[value_type](a,s)
        self.assertEqual(result, True)

    def template_any_empty(self, value_type):
        s=FROM_SET[value_type]([])
        a=array.array(BUFFER_SIZE[value_type],[])
        result=ANY[value_type](a,s)
        self.assertEqual(result, False)

    def template_any_empty_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=[]
        result=ANY_FROM_ITER[value_type](a,s)
        self.assertEqual(result, False)

    def template_any_empty_set(self, value_type):
        s=FROM_SET[value_type]([])
        a=array.array(BUFFER_SIZE[value_type],[1])
        result=ANY[value_type](a,s)
        self.assertEqual(result, False)

    def template_any_empty_set_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=[1]
        result=ANY_FROM_ITER[value_type](a,s)
        self.assertEqual(result, False)

    def template_noniter_from_iter(self, value_type):
        s=FROM_SET[value_type]([])
        a=1
        with self.assertRaises(TypeError) as context:
            ANY_FROM_ITER[value_type](a,s)
        self.assertTrue("object is not iterable" in context.exception.args[0])

    def template_memview_none(self, value_type):
        s=FROM_SET[value_type]([])
        self.assertEqual(ANY[value_type](None,s), False)

    def template_dbnone(self, value_type):
        a=array.array(BUFFER_SIZE[value_type],[1])
        self.assertEqual(ANY[value_type](a,None), False)

    def template_dbnone_from_iter(self, value_type):
        a=1
        self.assertEqual(ANY_FROM_ITER[value_type](a,None), False)


class AnyTesterPyObject(unittest.TestCase): 
    def test_any_no(self):
        s=PyObjectSet_from([2,4,666])
        a=np.array([1,3,333]*6, dtype=np.object)
        result=any_pyobject(a,s)
        self.assertEqual(result, False)

    def test_any_no_from_iter(self):
        s=PyObjectSet_from([2,4,666])
        a=[1,3,333]*6
        result=any_pyobject_from_iter(a,s)
        self.assertEqual(result, False)

    def test_any_last_yes(self):
        s=PyObjectSet_from([2,4,666])
        a=np.array([1,3,333]*6+[2], dtype=np.object)
        result=any_pyobject(a,s)
        self.assertEqual(result, True)

    def test_any_last_yes_from_iter(self):
        s=PyObjectSet_from([2,4,666])
        a=[1,3,333]*6+[2]
        result=any_pyobject_from_iter(a,s)
        self.assertEqual(result, True)

    def test_any_empty(self):
        s=PyObjectSet_from([])
        a=np.array([], dtype=np.object)
        result=any_pyobject(a,s)
        self.assertEqual(result, False)

    def test_any_empty_from_iter(self):
        s=PyObjectSet_from([])
        a=[]
        result=any_pyobject_from_iter(a,s)
        self.assertEqual(result, False)

    def test_any_empty_set(self):
        s=PyObjectSet_from([])
        a=np.array([1], dtype=np.object)
        result=any_pyobject(a,s)
        self.assertEqual(result, False)

    def test_any_empty_set_from_iter(self):
        s=PyObjectSet_from([])
        a=[1]
        result=any_pyobject_from_iter(a,s)
        self.assertEqual(result, False)

    def test_noniter_from_iter(self):
        s=PyObjectSet_from([])
        a=1
        with self.assertRaises(TypeError) as context:
            any_pyobject_from_iter(a,s)
        self.assertTrue("object is not iterable" in context.exception.args[0])

    def test_memview_none(self):
        s=PyObjectSet_from([])
        self.assertEqual(any_pyobject(None,s), False)

    def test_dbnone(self):
        a=np.array([1], dtype=np.object)
        self.assertEqual(any_pyobject(a,None), False)

    def test_dbnone_from_iter(self):
        a=1
        self.assertEqual(any_pyobject_from_iter(a,None), False)

 
