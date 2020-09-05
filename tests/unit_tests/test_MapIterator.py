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
        for x in cy_map.items():
         clone[x[0]] = x[1] 
        self.assertEqual(py_map, clone)

    def template_iterate_after_clear(self, map_type):
        cy_map = map_type(zip(range(1000), range(1000)))
        it = iter(cy_map.items())
        for x in range(1000):
            next(it)
        cy_map.clear()
        with self.assertRaises(StopIteration):
            next(it)

    def template_iterate_after_growing(self, map_type):
        cy_map = map_type()
        it = iter(cy_map.keys())
        #change bucket size
        for i in range(1000):
            cy_map[i]=i
        #make sure new size is used
        lst = []
        with self.assertRaises(StopIteration):
            for x in range(1001):
                lst.append(next(it))
        self.assertEqual(set(lst), set(range(1000)))

    def template_iterate_after_growing2(self, map_type):
        cy_map = map_type()
        cy_map[42]=42
        it = iter(cy_map.keys())
        next(it) #iterator shows to end now
        cy_map[11]=11
        cy_map[15]=15
        cy_map[13]=13
        #old end is no longer an end
        try:
            self.assertTrue(next(it) in {42,11,15,13})
        except StopIteration:
            pass # stop iteration could be an acceptable outcome
