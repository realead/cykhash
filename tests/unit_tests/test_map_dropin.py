import unittest
import uttemplate

from cykhash import Int64to64Map, Int32to32Map, Float64to64Map, Float32to32Map, PyObjectMap
import cykhash

nopython_maps = [Int64to64Map, Int32to32Map, Float64to64Map, Float32to32Map]
all_maps = nopython_maps + [PyObjectMap]


@uttemplate.from_templates(all_maps)
class MapDropinTester(unittest.TestCase): 
    def template_init_int_from_iter(self, set_type):
        m=set_type([(1,2),(3,1)])
        self.assertEqual(len(m), 2)
        self.assertEqual(m[1],2)
        self.assertTrue(m[3],1)

    @uttemplate.for_types(nopython_maps)
    def template_init_float_from_iter(self, set_type):
        m=set_type([(1,2.2),(3,1.3)], for_int=False)
        self.assertEqual(len(m), 2)
        self.assertAlmostEqual(m[1],2.2, delta=1e-5)
        self.assertAlmostEqual(m[3],1.3, delta=1e-5)

    @uttemplate.for_types(nopython_maps)
    def template_init_int_from_iter_with_floats(self, set_type):
        # float implements __int__, thus we use it
        m=set_type([(1,2),(3,1.3)], for_int=True)
        self.assertEqual(len(m), 2)
        self.assertEqual(m[1],2)
        self.assertEqual(m[3],1)

@uttemplate.from_templates(all_maps)
class DictViewTester(unittest.TestCase): 
    def template_init_int_from_iter(self, set_type):
        pass

   



