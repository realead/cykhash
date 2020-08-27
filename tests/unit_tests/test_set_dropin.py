import unittest
import uttemplate

from cykhash import Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet
import cykhash

SUFFIX={Int64Set : "int64",  
        Int32Set : "int32",  
        Float64Set : "float64",  
        Float32Set : "float32",  
        PyObjectSet : "pyobject"}
def pick_fun(name, set_type):
    return getattr(cykhash, name+"_"+SUFFIX[set_type])
    

@uttemplate.from_templates([Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet])
class SetDropInTester(unittest.TestCase): 

    def template_init_from_iter(self, set_type):
        s=set_type([1,2,3,1])
        self.assertEqual(len(s), 3)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)

@uttemplate.from_templates([Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet])
class IsDisjointTester(unittest.TestCase): 

    def template_aredisjoint_with_none(self, set_type):
        s=set_type([1,2,3,1])
        fun=pick_fun("aredisjoint", set_type)
        with self.assertRaises(TypeError) as context:
            fun(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])
        with self.assertRaises(TypeError) as context:
            fun(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])
        with self.assertRaises(TypeError) as context:
            fun(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])

    def template_aredisjoint_with_empty(self, set_type):
        empty1=set_type()
        empty2=set_type()
        non_empty=set_type(range(3))
        aredisjoint=pick_fun("aredisjoint", set_type)
        self.assertEqual(aredisjoint(empty1, non_empty), True)
        self.assertEqual(aredisjoint(non_empty, empty2), True)
        self.assertEqual(aredisjoint(empty1, empty2), True)

    def template_aredisjoint_yes(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([4,55])
        fun=pick_fun("aredisjoint", set_type)
        self.assertEqual(fun(a,b), True)
        self.assertEqual(fun(b,a), True)

    def template_aredisjoint_no(self, set_type):
        a=set_type([1,2,3,333,1])
        b=set_type([4,55,4,5,6,7,333])
        fun=pick_fun("aredisjoint", set_type)
        self.assertEqual(fun(a,b), False)
        self.assertEqual(fun(b,a), False)

    def template_isdisjoint_yes_set(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([4,55])
        self.assertEqual(a.isdisjoint(b), True)
        self.assertEqual(b.isdisjoint(a), True)

    def template_isdisjoint_no_set(self, set_type):
        a=set_type([1,2,3,333,1])
        b=set_type([4,55,4,5,6,7,333])
        self.assertEqual(a.isdisjoint(b), False)
        self.assertEqual(b.isdisjoint(a), False)

    def template_isdisjoint_yes_iter(self, set_type):
        a=set_type([1,2,3,1])
        b=[4,55]
        self.assertEqual(a.isdisjoint(b), True)

    def template_isdisjoint_no_iter(self, set_type):
        a=set_type([1,2,3,333,1])
        b=[4,55,4,5,6,7,333]
        self.assertEqual(a.isdisjoint(b), False)


@uttemplate.from_templates([Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet])
class IsSubsetIsSupersetTester(unittest.TestCase): 

    def template_with_none(self, set_type):
        s=set_type([1,2,3,1])
        fun=pick_fun("issubset", set_type)
        with self.assertRaises(TypeError) as context:
            fun(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])
        with self.assertRaises(TypeError) as context:
            fun(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])
        with self.assertRaises(TypeError) as context:
            fun(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.exception.args[0])

    def template_with_empty(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([])
        fun=pick_fun("issubset", set_type)
        self.assertEqual(fun(a,a), True)
        self.assertEqual(fun(a,b), True)
        self.assertEqual(fun(b,a), False)
        self.assertEqual(fun(b,b), True)

    def template_yes(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([1,3])
        fun=pick_fun("issubset", set_type)
        self.assertEqual(fun(a,b), True)
        self.assertEqual(fun(b,a), False)

    def template_no(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([4])
        fun=pick_fun("issubset", set_type)
        self.assertEqual(fun(a,b), False)
        self.assertEqual(fun(b,a), False)

    def template_issuperset_yes(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([1,3])
        self.assertEqual(a.issuperset(b), True)
        self.assertEqual(b.issuperset(a), False)

    def template_issuperset_no(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([4])
        self.assertEqual(a.issuperset(b), False)
        self.assertEqual(b.issuperset(a), False)

    def template_issuperset_yes_iter(self, set_type):
        a=set_type([1,2,3,1])
        b=[1,3]
        self.assertEqual(a.issuperset(b), True)

    def template_issuperset_no_iter(self, set_type):
        a=set_type([1,2,3,1])
        b=[4]
        self.assertEqual(a.issuperset(b), False)

    def template_issubset_yes_iter(self, set_type):
        a=set_type([1,2])
        b=[1,3,2]
        self.assertEqual(a.issubset(b), True)

    def template_issubset_no_iter(self, set_type):
        a=set_type([1,2])
        b=[1,1,3]
        self.assertEqual(a.issubset(b), False)

    def template_issubset_yes(self, set_type):
        a=set_type([1,2])
        b=set_type([1,3,2])
        self.assertEqual(a.issubset(b), True)
        self.assertEqual(b.issubset(a), False)

    def template_issubset_no(self, set_type):
        a=set_type([1,2])
        b=set_type([1,1,3])
        self.assertEqual(a.issubset(b), False)
        self.assertEqual(b.issubset(a), False)

    def template_compare_self(self, set_type):
        a=set_type([1,2])
        self.assertEqual(a<=a, True)
        self.assertEqual(a>=a, True)
        self.assertEqual(a<a, False)
        self.assertEqual(a>a, False)

    def template_compare_no_relation(self, set_type):
        a=set_type([1,2])
        b=set_type([1,3])
        self.assertEqual(a<=b, False)
        self.assertEqual(a>=b, False)
        self.assertEqual(a<b, False)
        self.assertEqual(a>b, False)

    def template_compare_real_subset(self, set_type):
        a=set_type([1,2,3])
        b=set_type([1,3])
        self.assertEqual(a<=b, False)
        self.assertEqual(a>=b, True)
        self.assertEqual(a<b, False)
        self.assertEqual(a>b, True)

    def template_compare_same(self, set_type):
        a=set_type([1,3])
        b=set_type([1,3])
        self.assertEqual(a<=b, True)
        self.assertEqual(a>=b, True)
        self.assertEqual(a<b, False)
        self.assertEqual(a>b, False)

    def template_compare_equal_yes(self, set_type):
        a=set_type([2,5,7,8,1,3])
        b=set_type([1,3,7,7,7,7,7,2,5,8,8,8,8,8,8])
        self.assertEqual(a==b, True)
        self.assertEqual(a==b, True)

    def template_compare_equal_yes(self, set_type):
        a=set_type([2,5,7,8,1,3])
        b=set_type([3,7,7,7,7,7,2,5,8,8,8,8,8,8])
        self.assertEqual(a==b, False)
        self.assertEqual(a==b, False)


@uttemplate.from_templates([Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet])
class CopyTester(unittest.TestCase): 

    def template_with_none(self, set_type):
        s=set_type([1,2,3,1])
        copy=pick_fun("copy", set_type)
        self.assertTrue(copy(None) is None)

    def template_with_empty(self, set_type):
        a=set_type([])
        copy=pick_fun("copy", set_type)
        self.assertEqual(len(copy(a)), 0)

    def template_small(self, set_type):
        a=set_type([1,2,3,1])
        copy=pick_fun("copy", set_type)
        self.assertEqual(copy(a)==a, True)

    def template_large(self, set_type):
        a=set_type(range(33,10000,3))
        copy=pick_fun("copy", set_type)
        self.assertEqual(copy(a)==a, True)

    def template_large_method(self, set_type):
        a=set_type(range(33,10000,3))
        self.assertEqual(a.copy()==a, True)


