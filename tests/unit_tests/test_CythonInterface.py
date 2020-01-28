import pyximport; 
pyximport.install(setup_args = {"script_args" : ["--force"]},
                  language_level=3)

import unittest
import cyinterfacetester as cyt
from cykhash import Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet


#just making sure the interface can be accessed:

class CyIntegerfaceTester(unittest.TestCase): 

   def test_cimport_works_i64(self):
      received=cyt.isin_int64([1,2,3,4], [2,4])
      expected=[False, True, False, True]
      self.assertEqual(received, expected)

   def test_iter_interface_works_i64(self):
      cy_set = Int64Set()
      py_set = set()
      for i in range(10):
         cy_set.add(i)
         py_set.add(i)
      clone = cyt.as_py_set_int64(cy_set)
      self.assertEqual(py_set, clone)

### -------------------------------

   def test_cimport_works_i32(self):
      received=cyt.isin_int32([1,2,3,4], [2,4])
      expected=[False, True, False, True]
      self.assertEqual(received, expected)

   def test_iter_interface_works_i32(self):
      cy_set = Int32Set()
      py_set = set()
      for i in range(10):
         cy_set.add(i)
         py_set.add(i)
      clone = cyt.as_py_set_int32(cy_set)
      self.assertEqual(py_set, clone)
    
### -------------------------------

   def test_cimport_works_f64(self):
      received=cyt.isin_float64([1,2,3,4], [2,4])
      expected=[False, True, False, True]
      self.assertEqual(received, expected)

   def test_iter_interface_works_f64(self):
      cy_set = Float64Set()
      py_set = set()
      for i in range(10):
         cy_set.add(i)
         py_set.add(i)
      clone = cyt.as_py_set_float64(cy_set)
      self.assertEqual(py_set, clone)  


### -------------------------------

   def test_cimport_works_f32(self):
      received=cyt.isin_float32([1,2,3,4], [2,4])
      expected=[False, True, False, True]
      self.assertEqual(received, expected)

   def test_iter_interface_works_f32(self):
      cy_set = Float32Set()
      py_set = set()
      for i in range(10):
         cy_set.add(i)
         py_set.add(i)
      clone = cyt.as_py_set_float32(cy_set)
      self.assertEqual(py_set, clone)        

### -------------------------------

   def test_cimport_works_pyobject(self):
      received=cyt.isin_pyobject([1,2,3,4], [2,4])
      expected=[False, True, False, True]
      self.assertEqual(received, expected)

   def test_iter_interface_works_pyobject(self):
      cy_set = PyObjectSet()
      py_set = set()
      for i in range(10):
         cy_set.add(i)
         py_set.add(i)
      clone = cyt.as_py_set_pyobject(cy_set)
      self.assertEqual(py_set, clone)     
      

