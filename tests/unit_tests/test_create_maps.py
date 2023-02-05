from unittestmock import UnitTestMock
import pytest

import array

from cykhash import Int64toInt64Map_from_buffers, Int64toFloat64Map_from_buffers
from cykhash import Int32toInt32Map_from_buffers, Int32toFloat32Map_from_buffers
from cykhash import Float64toInt64Map_from_buffers, Float64toFloat64Map_from_buffers
from cykhash import Float32toInt32Map_from_buffers, Float32toFloat32Map_from_buffers
from cykhash import PyObjectMap_from_buffers

FUNCTION = {'int64_int64':   Int64toInt64Map_from_buffers,
            'int64_float64': Int64toFloat64Map_from_buffers,
            'int32_int32':   Int32toInt32Map_from_buffers,
            'int32_float32': Int32toFloat32Map_from_buffers,
            'float64_int64':   Float64toInt64Map_from_buffers,
            'float64_float64': Float64toFloat64Map_from_buffers,
            'float32_int32':   Float32toInt32Map_from_buffers,
            'float32_float32': Float32toFloat32Map_from_buffers,
           }
KEY_FORMAT = {'int64_int64':   'q',
              'int64_float64': 'q',
              'int32_int32':   'i',
              'int32_float32': 'i',
              'float64_int64':   'd',
              'float64_float64': 'd',
              'float32_int32':   'f',
              'float32_float32': 'f',
             }
VAL_FORMAT = {'int64_int64':   'q',
              'int64_float64': 'd',
              'int32_int32':   'i',
              'int32_float32': 'f',
              'float64_int64':   'q',
              'float64_float64': 'd',
              'float32_int32':   'i',
              'float32_float32': 'f',
             }


@pytest.mark.parametrize(
    "fun_type",
    ['int64_int64', 'int64_float64',
    'int32_int32', 'int32_float32',
    'float64_int64', 'float64_float64',
    'float32_int32', 'float32_float32',
   ])
class TestMap_from_buffer(UnitTestMock):
    def test_create_from(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6])
        m=FUNCTION[fun_type](keys, vals, 2.0)
        self.assertEqual(len(m), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)

    def test_create_diff_vals_longer(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6,7])
        m=FUNCTION[fun_type](keys, vals, 2.0)
        self.assertEqual(len(m), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)

    def test_create_diff_keys_longer(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3,42])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6])
        m=FUNCTION[fun_type](keys, vals, 2.0)
        self.assertEqual(len(m), len(vals))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)


class TestPyObject_from_buffers(UnitTestMock): 
    def test_pyobject_create_from(self):
        try:
            import numpy as np
        except:
            return # well what should I do?
        keys=np.array([1,2,3], dtype=np.object_)
        vals=np.array([4,5,6], dtype=np.object_)
        m=PyObjectMap_from_buffers(keys, vals, 2.0)
        self.assertEqual(len(m), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)

    def test_create_diff_vals_longer(self):
        try:
            import numpy as np
        except:
            return # well what should I do?
        keys=np.array([1,2,3], dtype=np.object_)
        vals=np.array([4,5,6,7], dtype=np.object_)
        m=PyObjectMap_from_buffers(keys, vals, 2.0)
        self.assertEqual(len(m), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)


    def test_create_diff_keys_longer(self):
        try:
            import numpy as np
        except:
            return # well what should I do?
        keys=np.array([1,2,3, 42], dtype=np.object_)
        vals=np.array([4,5,6], dtype=np.object_)
        m=PyObjectMap_from_buffers(keys, vals, 2.0)
        self.assertEqual(len(m), len(vals))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)


