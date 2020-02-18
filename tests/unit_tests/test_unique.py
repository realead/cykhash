import unittest
import uttemplate

import pyximport; 
pyximport.install(setup_args = {"script_args" : ["--force"]},
                  language_level=3)

from cykhash import unique_int64, unique_int32, unique_float64, unique_float32
from uniqueinterfacetester import use_unique_int64, use_unique_int32, use_unique_float64, use_unique_float32

UNIQUE={'int64': unique_int64,
        'int32': unique_int32,
        'float64': unique_float64,
        'float32': unique_float32,
       }

CY_UNIQUE={'int64': use_unique_int64,
           'int32': use_unique_int32,
           'float64': use_unique_float64,
           'float32': use_unique_float32,
       }

BUFFER_SIZE = {'int32': 'i', 'int64': 'q', 'float64' : 'd', 'float32' : 'f'}


import array
@uttemplate.from_templates(['int64', 'int32', 'float64', 'float32'])
class UniqueTester(unittest.TestCase): 
    def template_unique(self, value_type):
        a = array.array(BUFFER_SIZE[value_type], [1,1,1,1,1,2,3,4,5])
        result = UNIQUE[value_type](a)
        as_set = set(memoryview(result))
        expected = set(array.array(BUFFER_SIZE[value_type], [1,2,3,4,5]))
        self.assertTrue(expected==as_set, msg = "received: "+str(as_set))


    def template_unique2(self, value_type):
        a = array.array(BUFFER_SIZE[value_type], list(range(100))+list(range(200))+list(range(100)))
        result = UNIQUE[value_type](a)
        as_set = set(memoryview(result))
        expected = set(array.array(BUFFER_SIZE[value_type], range(200)))
        self.assertTrue(expected==as_set, msg = "received: "+str(as_set))


    def template_cyunique(self, value_type):
        a = array.array(BUFFER_SIZE[value_type], list(range(100))+list(range(200))+list(range(100)))
        result = CY_UNIQUE[value_type](a)
        as_set = set(memoryview(result))
        expected = set(array.array(BUFFER_SIZE[value_type], range(200)))
        self.assertTrue(expected==as_set, msg = "received: "+str(as_set))

 
