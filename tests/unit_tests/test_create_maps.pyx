import unittest
import uttemplate

from cykhash import Int64to64Map_from_int64_buffer, Int64to64Map_from_float64_buffer

FUNCTION = {'int64_int64':   Int64to64Map_from_int64_buffer,
            'int64_float64': Int64to64Map_from_float64_buffer,
           }
KEY_FORMAT = {'int64_int64':   'q',
              'int64_float64': 'q',
             }
VAL_FORMAT = {'int64_int64':   'q',
              'int64_float64': 'd',
             }


@uttemplate.from_templates(['int64_int64', 'int64_float64'])
class Map_from_buffer_Tester(unittest.TestCase):
    def template_create_from(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6])
        m=FUNCTION[value_type](keys, vals, 2.0)
        self.assertEqual(len(s), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)

    def template_create_diff_vals_longer(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6,7])
        m=FUNCTION[value_type](keys, vals, 2.0)
        self.assertEqual(len(s), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)

    def template_create_diff_keys_longer(self, fun_type):
        keys=array.array(KEY_FORMAT[fun_type], [1,2,3,42])
        vals=array.array(VAL_FORMAT[fun_type], [4,5,6])
        m=FUNCTION[value_type](keys, vals, 2.0)
        self.assertEqual(len(s), len(keys))
        for x,y in zip(keys, vals):
            self.assertTrue(x in m)
            self.assertEqual(m[x], y)


