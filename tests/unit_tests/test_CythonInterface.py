import pyximport; pyximport.install()

import unittest
import cyinterfacetester as cyt


#just making sure the interface can be accessed:

class CyIntegerfaceTester(unittest.TestCase): 

   def test_cimport_works(self):
      received=cyt.isin([1,2,3,4], [2,4])
      expected=[False, True, False, True]
      self.assertEqual(received, expected)

