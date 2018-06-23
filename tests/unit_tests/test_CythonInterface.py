import pyximport; pyximport.install()

import unittest
import cyinterfacetester as cyt
from cykhash import Int64Set, Int32Set


#just making sure the interface can be accessed:

class CyIntegerfaceTester(unittest.TestCase): 

   def test_cimport_works64(self):
      received=cyt.isin_int64([1,2,3,4], [2,4])
      expected=[False, True, False, True]
      self.assertEqual(received, expected)

   def test_iter_interface_works64(self):
      cy_set = Int64Set()
      py_set = set()
      for i in range(10):
         cy_set.add(i)
         py_set.add(i)
      clone = cyt.as_py_set_int64(cy_set)
      self.assertEqual(py_set, clone)

### -------------------------------

   def test_cimport_works32(self):
      received=cyt.isin_int32([1,2,3,4], [2,4])
      expected=[False, True, False, True]
      self.assertEqual(received, expected)

   def test_iter_interface_works32(self):
      cy_set = Int32Set()
      py_set = set()
      for i in range(10):
         cy_set.add(i)
         py_set.add(i)
      clone = cyt.as_py_set_int32(cy_set)
      self.assertEqual(py_set, clone)
    
        

