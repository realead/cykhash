import unittest
import uttemplate

from cykhash import Int64to64Map

@uttemplate.from_templates([Int64to64Map])
class MapIteratorTester(unittest.TestCase): 

   def template_iterate(self, map_type):
      cy_map = map_type()
      py_map = dict()
      for i in range(10):
         cy_map.put_int64(i, i+1)
         py_map[i] = i+1
      clone = dict()
      for x in cy_map:
         clone[x['key']] = x['val'] 
      self.assertEqual(py_map, clone)

