import unittest

from cykhash import Int64Set



class Int64IteratorTester(unittest.TestCase): 

   def test_iterate(self):
      cy_set = Int64Set()
      py_set = set()
      for i in range(10):
         cy_set.add(i)
         py_set.add(i)
      clone = set()
      for x in cy_set:
         clone.add(x)
      self.assertEqual(py_set, clone)

