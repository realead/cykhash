import unittest
import uttemplate

from cykhash import isin_int64, Int64Set_from
from cykhash import isin_int32, Int32Set_from
from cykhash import isin_float64, Float64Set_from
from cykhash import isin_float32, Float32Set_from
from cykhash import isin_pyobject,  PyObjectSet_from

ISIN={'int32': isin_int32, 'int64': isin_int64, 'float64' : isin_float64, 'float32' : isin_float32}
FROM_SET={'int32': Int32Set_from, 'int64': Int64Set_from, 'float64' : Float64Set_from, 'float32' : Float32Set_from, 'pyobject' : PyObjectSet_from}
BUFFER_SIZE = {'int32': 'i', 'int64': 'l', 'float64' : 'd', 'float32' : 'f'}



@uttemplate.from_templates(['int64', 'int32', 'float64', 'float32', 'pyobject'])
class Int64Set_from_Tester(unittest.TestCase):
    def template_create(self, value_type):
        lst=[6,7,8]
        s=FROM_SET[value_type](list(lst))
        self.assertEqual(len(s), len(lst))
        for x in lst:
            self.assertTrue(x in s)


import array
@uttemplate.from_templates(['int64', 'int32', 'float64', 'float32'])
class IsInTester(unittest.TestCase): 
    def template_isin(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], range(0,7))
        result=array.array('B', [False]*7)
        ISIN[value_type](a,s,result)
        expected=array.array('B', [False, False, True, False, True, False, True])
        self.assertTrue(expected==result)


class IsInTesterPyObject(unittest.TestCase): 
    def test_pyobject_isin(self):
        try:
            import numpy as np
        except:
            return # well what should I do?
        s=PyObjectSet_from([2,4,6])
        a=np.array(range(0,7), dtype=np.object)
        result=array.array('B', [False]*7)
        isin_pyobject(a,s,result)
        expected=array.array('B', [False, False, True, False, True, False, True])
        self.assertTrue(expected==result)
 
