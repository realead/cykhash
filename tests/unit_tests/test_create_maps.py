import unittest
import uttemplate
import array

from cykhash import Int64to64Map_from_int64_buffer, Int64to64Map_from_float64_buffer
from cykhash import Int32to32Map_from_int32_buffer, Int32to32Map_from_float32_buffer
from cykhash import Float64to64Map_from_int64_buffer, Float64to64Map_from_float64_buffer
from cykhash import Float32to32Map_from_int32_buffer, Float32to32Map_from_float32_buffer

FUNCTION = {'int64_int64':   Int64to64Map_from_int64_buffer,
            'int64_float64': Int64to64Map_from_float64_buffer,
            'int32_int32':   Int32to32Map_from_int32_buffer,
            'int32_float32': Int32to32Map_from_float32_buffer,
            'float64_int64':   Float64to64Map_from_int64_buffer,
            'float64_float64': Float64to64Map_from_float64_buffer,
            'float32_int32':   Float32to32Map_from_int32_buffer,
            'float32_float32': Float32to32Map_from_float32_buffer,
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


@uttemplate.from_templates(['int64_int64', 'int64_float64',
                            'int32_int32', 'int32_float32',
                            'float64_int64', 'float64_float64',
                            'float32_int32', 'float32_float32',
                           ])
class Map_from_buffer_Tester(unittest.TestCase):
    def template_create_from(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6])
        m=FUNCTION[fun_type](keys, vals, 2.0)
        self.assertEqual(len(m), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)

    def template_create_diff_vals_longer(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6,7])
        m=FUNCTION[fun_type](keys, vals, 2.0)
        self.assertEqual(len(m), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)

    def template_create_diff_keys_longer(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3,42])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6])
        m=FUNCTION[fun_type](keys, vals, 2.0)
        self.assertEqual(len(m), len(vals))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)


