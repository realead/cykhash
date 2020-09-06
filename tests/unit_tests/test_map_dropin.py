import unittest
import uttemplate

from cykhash import Int64to64Map, Int32to32Map, Float64to64Map, Float32to32Map, PyObjectMap
import cykhash

nopython_maps = [Int64to64Map, Int32to32Map, Float64to64Map, Float32to32Map]
all_maps = nopython_maps + [PyObjectMap]

SUFFIX={Int64to64Map : "int64map",  
        Int32to32Map : "int32map",  
        Float64to64Map : "float64map",  
        Float32to32Map : "float32map",  
        PyObjectMap : "pyobjectmap"}
def pick_fun(name, set_type):
    return getattr(cykhash, name+"_"+SUFFIX[set_type])


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

    def template_clear(self, set_type):
        a=set_type([(1,2), (2,3)])      
        a.clear()
        self.assertEqual(len(a), 0)
        a[5]=6
        self.assertEqual(a[5], 6)
        a.clear()
        self.assertEqual(len(a), 0)

    def template_iterable(self, set_type):
        a=set_type([(1,4), (2,3)])      
        keys = list(a)
        self.assertEqual(set(keys), {1,2})

    def template_set_get_delete(self, set_type):
        a=set_type()      
        a[5] = 42
        self.assertEqual(len(a), 1)
        self.assertTrue(a)
        self.assertEqual(a[5], 42)
        del a[5]
        self.assertEqual(len(a), 0)
        self.assertFalse(a)
        with self.assertRaises(KeyError) as context:
            a[5]
        self.assertEqual(context.exception.args[0], 5)
        with self.assertRaises(KeyError) as context:
            a[5]
        self.assertEqual(context.exception.args[0], 5)
        


@uttemplate.from_templates(all_maps)
class SwapTester(unittest.TestCase): 
    def template_with_none(self, set_type):
        swap=pick_fun("swap", set_type)
        a=set_type([(1,2),(3,1)])
        with self.assertRaises(TypeError) as context:
            swap(None,a)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])
        with self.assertRaises(TypeError) as context:
            swap(a,None)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])
        with self.assertRaises(TypeError) as context:
            swap(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])


    def template_swap(self, set_type):
        swap=pick_fun("swap", set_type)
        a=set_type([(1,2),(3,1),(5,3)])
        b=set_type([(2,3),(4,6)])
        swap(a,b)
        self.assertEqual(len(a), 2)
        self.assertEqual(a[2], 3)
        self.assertEqual(a[4], 6)
        self.assertEqual(len(b), 3)
        self.assertEqual(b[1], 2)
        self.assertEqual(b[3], 1)
        self.assertEqual(b[5], 3)

    def template_empty(self, set_type):
        swap=pick_fun("swap", set_type)
        a=set_type(zip(range(1000), range(1000)))
        b=set_type()
        swap(a,b)
        self.assertEqual(len(a), 0)
        self.assertEqual(len(b), 1000)
        a[6]=3
        self.assertEqual(len(a), 1)
        b[1000]=0
        self.assertEqual(len(b), 1001)


    @uttemplate.for_types(nopython_maps)
    def template_swap_for_int(self, set_type):
        swap=pick_fun("swap", set_type)
        a=set_type([(1,2)])
        b=set_type([(2,3.3)], for_int=False)
        swap(a,b)
        self.assertEqual(len(a), 1)
        self.assertAlmostEqual(a[2],3.3, delta=1e-5)
        self.assertEqual(len(b), 1)
        self.assertEqual(b[1], 2)



@uttemplate.from_templates(all_maps)
class DictViewTester(unittest.TestCase): 
    def template_len(self, set_type):
        a=set_type([(1,2),(3,1),(5,3)])
        self.assertEqual(len(a.keys()), 3)
        self.assertEqual(len(a.items()), 3)
        self.assertEqual(len(a.values()), 3)

    def template_in(self, set_type):
        a=set_type([(1,2),(3,1),(5,3)])
        self.assertEqual(5 in a.keys(), True)
        self.assertEqual(6 in a.keys(), False)
        self.assertEqual(2 in a.values(), True)
        self.assertEqual(6 in a.values(), False)
        self.assertEqual((3,1) in a.items(), True)
        self.assertEqual((5,5) in a.items(), False)

   



