import unittest

from cykhash import isin, Int64Set_from


class Int64Set_from_Tester(unittest.TestCase):
    def test_create(self):
        lst=[6,7,8]
        s=Int64Set_from(list(lst))
        self.assertEqual(len(s), len(lst))
        for x in lst:
            self.assertTrue(x in s)


import array
class IsInTester(unittest.TestCase): 

    def test_isin(self):
        s=Int64Set_from([2,4,6])
        a=array.array('l', range(0,7))
        result=array.array('B', [False]*7)
        isin(a,s,result)
        expected=array.array('B', [False, False, True, False, True, False, True])
        self.assertTrue(expected==result)
 
