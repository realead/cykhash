import unittest
import uttemplate

from cykhash import Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet

@uttemplate.from_templates([Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet])
class SetIteratorTester(unittest.TestCase): 

    def template_iterate(self, set_type):
        cy_set = set_type()
        py_set = set()
        for i in range(10):
         cy_set.add(i)
         py_set.add(i)
        clone = set()
        for x in cy_set:
         clone.add(x)
        self.assertEqual(py_set, clone)

    def template_iterate_after_clear(self, set_type):
        cy_set = set_type(range(1000))
        it = iter(cy_set)
        for x in range(1000):
            next(it)
        cy_set.clear()
        with self.assertRaises(StopIteration):
            next(it)

