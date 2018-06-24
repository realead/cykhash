import unittest
import uttemplate

from cykhash import Int64Set, Int32Set, Float64Set, Float32Set

@uttemplate.from_templates([Int64Set, Int32Set, Float64Set, Float32Set])
class Int64IteratorTester(unittest.TestCase): 

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

