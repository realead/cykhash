import pyximport; 
pyximport.install(setup_args = {"script_args" : ["--force"]},
                  language_level=3)

import unittest
import cymapinterfacetester as cyt
from cykhash import Int64to64Map


#just making sure the interface can be accessed:

class CyMypInterfaceTester(unittest.TestCase): 

   def test_cimport_use_int64(self):
      received=cyt.use_int64([1,2,3,4], [5,6,7,8], [2,3])
      expected=[6,7]
      self.assertEqual(received, expected)

   def test_cimport_use_float64(self):
      received=cyt.use_float64([1,2,3,4], [5.5,6.5,7.5,8.5], [2,3])
      expected=[6.5,7.5]
      self.assertEqual(received, expected)

   def test_as_py_list_int64(self):
      cy_map = Int64to64Map()
      cy_map.put_int64(3, 20)
      lst = cyt.as_py_list_int64(cy_map)
      self.assertEqual(lst, [3,20])


   def test_as_py_list_int64_2(self):
      cy_map = Int64to64Map()
      cy_map.put_int64(3, 5)
      cy_map.put_int64(4, 6)
      lst = cyt.as_py_list_int64(cy_map)
      self.assertEqual(set(lst), set([3,4,5,6]))

    
      

