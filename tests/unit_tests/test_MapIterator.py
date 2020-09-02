import unittest
import uttemplate

from cykhash import Int64to64Map, Int32to32Map, Float64to64Map, Float32to32Map, PyObjectMap

@uttemplate.from_templates([Int64to64Map, Int32to32Map, Float64to64Map, Float32to32Map, PyObjectMap])
class MapIteratorTester(unittest.TestCase): 

    def template_iterate(self, map_type):
        cy_map = map_type()
        py_map = dict()
        for i in range(10):
         cy_map[i] = i+1
         py_map[i] = i+1
        clone = dict()
        for x in cy_map:
         clone[x['key']] = x['val'] 
        self.assertEqual(py_map, clone)

    def template_iterate_after_clear(self, set_type):
        cy_set = set_type(zip(range(1000), range(1000)))
        it = iter(cy_set)
        for x in range(1000):
            next(it)
        cy_set.clear()
        with self.assertRaises(StopIteration):
            next(it)

