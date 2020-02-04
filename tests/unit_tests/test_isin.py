import unittest
import uttemplate

from cykhash import isin_int64, Int64Set_from, Int64Set_from_buffer
from cykhash import isin_int32, Int32Set_from, Int32Set_from_buffer
from cykhash import isin_float64, Float64Set_from, Float64Set_from_buffer
from cykhash import isin_float32, Float32Set_from, Float32Set_from_buffer
from cykhash import isin_pyobject,  PyObjectSet_from, PyObjectSet_from_buffer

ISIN={'int32': isin_int32, 'int64': isin_int64, 'float64' : isin_float64, 'float32' : isin_float32}
FROM_SET={'int32': Int32Set_from, 'int64': Int64Set_from, 'float64' : Float64Set_from, 'float32' : Float32Set_from, 'pyobject' : PyObjectSet_from}
BUFFER_SIZE = {'int32': 'i', 'int64': 'q', 'float64' : 'd', 'float32' : 'f'}
FROM_BUFFER_SET={'int32': Int32Set_from_buffer, 'int64': Int64Set_from_buffer, 'float64' : Float64Set_from_buffer, 'float32' : Float32Set_from_buffer, 'pyobject' : PyObjectSet_from_buffer}


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
class BufferTester(unittest.TestCase): 
    def template_isin(self, value_type):
        s=FROM_SET[value_type]([2,4,6])
        a=array.array(BUFFER_SIZE[value_type], range(0,7))
        result=array.array('B', [False]*7)
        ISIN[value_type](a,s,result)
        expected=array.array('B', [False, False, True, False, True, False, True])
        self.assertTrue(expected==result)

    def template_from_buffer(self, value_type):
        a=array.array(BUFFER_SIZE[value_type], [6,7,8])
        s=FROM_BUFFER_SET[value_type](a)
        self.assertEqual(len(s), len(a))
        for x in a:
            self.assertTrue(x in s)


class BufferTesterPyObject(unittest.TestCase): 
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

    def test_pyobject_from_buffer(self):
        try:
            import numpy as np
        except:
            return # well what should I do?
        a=np.array([6,7,8], dtype=np.object)
        s=PyObjectSet_from_buffer(a)
        self.assertEqual(len(s), len(a))
        for x in a:
            self.assertTrue(x in s)
 
