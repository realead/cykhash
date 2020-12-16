import pytest
from unittestmock import UnitTestMock


from cykhash import Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet
import cykhash

SUFFIX={Int64Set : "int64",  
        Int32Set : "int32",  
        Float64Set : "float64",  
        Float32Set : "float32",  
        PyObjectSet : "pyobject"}
def pick_fun(name, set_type):
    return getattr(cykhash, name+"_"+SUFFIX[set_type])
    


@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestSetDropIn(UnitTestMock): 

    def test_init_from_iter(self, set_type):
        s=set_type([1,2,3,1])
        self.assertEqual(len(s), 3)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)

    def test_clear(self, set_type):
        s=set_type([1,2,3,1])
        s.clear()
        self.assertEqual(len(s), 0)
        s.add(5)
        s.update([3,4,5,6])
        self.assertEqual(s, set_type([3,4,5,6]))
        s.clear()
        self.assertEqual(len(s), 0)

    def test_str(self, set_type):
        s=set_type([1,2,3,1])
        ss = str(s)
        self.assertTrue("1" in ss)
        self.assertTrue("2" in ss)
        self.assertTrue("3" in ss)
        self.assertTrue(ss.startswith("{"))
        self.assertTrue(ss.endswith("}"))

    def test_remove_yes(self, set_type):
        s=set_type([1,2])
        s.remove(1)
        self.assertEqual(s,set_type([2]))
        s.remove(2)
        self.assertEqual(s,set_type([]))

    def test_remove_no(self, set_type):
        s=set_type([1,2])
        with pytest.raises(KeyError) as context:
            s.remove(3)
        self.assertEqual(3, context.value.args[0])

    def test_pop_one(self, set_type):
        s=set_type([1])
        el=s.pop()
        self.assertEqual(s,set_type([]))
        self.assertEqual(el,1)

    def test_pop_all(self, set_type):
        s=set_type([1,2,3])
        new_s={s.pop(), s.pop(), s.pop()}
        self.assertEqual(s,set_type([]))
        self.assertEqual(new_s,{1,2,3})

    def test_pop_empty(self, set_type):
        s=set_type([])
        with pytest.raises(KeyError) as context:
            s.pop()
        self.assertEqual("pop from empty set", context.value.args[0])

def test_pyobject_same_object_pop():
    a=float("3333.2")
    s=PyObjectSet([a])
    b=s.pop()
    assert a is b



@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestIsDisjoint(UnitTestMock): 

    def test_aredisjoint_with_none(self, set_type):
        s=set_type([1,2,3,1])
        fun=pick_fun("aredisjoint", set_type)
        with pytest.raises(TypeError) as context:
            fun(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            fun(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            fun(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])

    def test_aredisjoint_with_empty(self, set_type):
        empty1=set_type()
        empty2=set_type()
        non_empty=set_type(range(3))
        aredisjoint=pick_fun("aredisjoint", set_type)
        self.assertEqual(aredisjoint(empty1, non_empty), True)
        self.assertEqual(aredisjoint(non_empty, empty2), True)
        self.assertEqual(aredisjoint(empty1, empty2), True)

    def test_aredisjoint_yes(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([4,55])
        fun=pick_fun("aredisjoint", set_type)
        self.assertEqual(fun(a,b), True)
        self.assertEqual(fun(b,a), True)

    def test_aredisjoint_no(self, set_type):
        a=set_type([1,2,3,333,1])
        b=set_type([4,55,4,5,6,7,333])
        fun=pick_fun("aredisjoint", set_type)
        self.assertEqual(fun(a,b), False)
        self.assertEqual(fun(b,a), False)

    def test_isdisjoint_yes_set(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([4,55])
        self.assertEqual(a.isdisjoint(b), True)
        self.assertEqual(b.isdisjoint(a), True)

    def test_isdisjoint_no_set(self, set_type):
        a=set_type([1,2,3,333,1])
        b=set_type([4,55,4,5,6,7,333])
        self.assertEqual(a.isdisjoint(b), False)
        self.assertEqual(b.isdisjoint(a), False)

    def test_isdisjoint_yes_iter(self, set_type):
        a=set_type([1,2,3,1])
        b=[4,55]
        self.assertEqual(a.isdisjoint(b), True)

    def test_isdisjoint_no_iter(self, set_type):
        a=set_type([1,2,3,333,1])
        b=[4,55,4,5,6,7,333]
        self.assertEqual(a.isdisjoint(b), False)


@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestIsSubsetIsSuperset(UnitTestMock): 

    def test_with_none(self, set_type):
        s=set_type([1,2,3,1])
        fun=pick_fun("issubset", set_type)
        with pytest.raises(TypeError) as context:
            fun(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            fun(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            fun(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])

    def test_with_empty(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([])
        fun=pick_fun("issubset", set_type)
        self.assertEqual(fun(a,a), True)
        self.assertEqual(fun(a,b), True)
        self.assertEqual(fun(b,a), False)
        self.assertEqual(fun(b,b), True)

    def test_yes(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([1,3])
        fun=pick_fun("issubset", set_type)
        self.assertEqual(fun(a,b), True)
        self.assertEqual(fun(b,a), False)

    def test_no(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([4])
        fun=pick_fun("issubset", set_type)
        self.assertEqual(fun(a,b), False)
        self.assertEqual(fun(b,a), False)

    def test_issuperset_yes(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([1,3])
        self.assertEqual(a.issuperset(b), True)
        self.assertEqual(b.issuperset(a), False)

    def test_issuperset_no(self, set_type):
        a=set_type([1,2,3,1])
        b=set_type([4])
        self.assertEqual(a.issuperset(b), False)
        self.assertEqual(b.issuperset(a), False)

    def test_issuperset_yes_iter(self, set_type):
        a=set_type([1,2,3,1])
        b=[1,3]
        self.assertEqual(a.issuperset(b), True)

    def test_issuperset_no_iter(self, set_type):
        a=set_type([1,2,3,1])
        b=[4]
        self.assertEqual(a.issuperset(b), False)

    def test_issubset_yes_iter(self, set_type):
        a=set_type([1,2])
        b=[1,3,2]
        self.assertEqual(a.issubset(b), True)

    def test_issubset_no_iter(self, set_type):
        a=set_type([1,2])
        b=[1,1,3]
        self.assertEqual(a.issubset(b), False)

    def test_issubset_yes(self, set_type):
        a=set_type([1,2])
        b=set_type([1,3,2])
        self.assertEqual(a.issubset(b), True)
        self.assertEqual(b.issubset(a), False)

    def test_issubset_no(self, set_type):
        a=set_type([1,2])
        b=set_type([1,1,3])
        self.assertEqual(a.issubset(b), False)
        self.assertEqual(b.issubset(a), False)

    def test_compare_self(self, set_type):
        a=set_type([1,2])
        self.assertEqual(a<=a, True)
        self.assertEqual(a>=a, True)
        self.assertEqual(a<a, False)
        self.assertEqual(a>a, False)

    def test_compare_no_relation(self, set_type):
        a=set_type([1,2])
        b=set_type([1,3])
        self.assertEqual(a<=b, False)
        self.assertEqual(a>=b, False)
        self.assertEqual(a<b, False)
        self.assertEqual(a>b, False)

    def test_compare_real_subset(self, set_type):
        a=set_type([1,2,3])
        b=set_type([1,3])
        self.assertEqual(a<=b, False)
        self.assertEqual(a>=b, True)
        self.assertEqual(a<b, False)
        self.assertEqual(a>b, True)

    def test_compare_same(self, set_type):
        a=set_type([1,3])
        b=set_type([1,3])
        self.assertEqual(a<=b, True)
        self.assertEqual(a>=b, True)
        self.assertEqual(a<b, False)
        self.assertEqual(a>b, False)

    def test_compare_equal_yes(self, set_type):
        a=set_type([2,5,7,8,1,3])
        b=set_type([1,3,7,7,7,7,7,2,5,8,8,8,8,8,8])
        self.assertEqual(a==b, True)
        self.assertEqual(a==b, True)

    def test_compare_equal_yes(self, set_type):
        a=set_type([2,5,7,8,1,3])
        b=set_type([3,7,7,7,7,7,2,5,8,8,8,8,8,8])
        self.assertEqual(a==b, False)
        self.assertEqual(a==b, False)


@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestCopy(UnitTestMock): 

    def test_with_none(self, set_type):
        s=set_type([1,2,3,1])
        copy=pick_fun("copy", set_type)
        self.assertTrue(copy(None) is None)

    def test_with_empty(self, set_type):
        a=set_type([])
        copy=pick_fun("copy", set_type)
        self.assertEqual(len(copy(a)), 0)

    def test_small(self, set_type):
        a=set_type([1,2,3,1])
        copy=pick_fun("copy", set_type)
        self.assertEqual(copy(a)==a, True)

    def test_large(self, set_type):
        a=set_type(range(33,10000,3))
        copy=pick_fun("copy", set_type)
        self.assertEqual(copy(a)==a, True)

    def test_large_method(self, set_type):
        a=set_type(range(33,10000,3))
        self.assertEqual(a.copy()==a, True)


@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestUpdate(UnitTestMock): 

    def test_with_none(self, set_type):
        s=set_type([1,2,3,1])
        update=pick_fun("update", set_type)        
        with pytest.raises(TypeError) as context:
            update(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            update(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            update(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])

    def test_some_common(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([2,1,2,5])
        c=b.copy()
        update=pick_fun("update", set_type) 
        update(a,b)
        self.assertEqual(a, set_type([1,2,3,4,5]))
        self.assertEqual(b, c)

    def test_with_itself(self, set_type):
        a=set_type([1,2,3,1])
        b=a.copy()
        update=pick_fun("update", set_type) 
        update(a,a)
        self.assertEqual(a, b)

    def test_with_disjunct(self, set_type):
        a=set_type(range(50))
        b=set_type(range(50,100))
        update=pick_fun("update", set_type) 
        update(a,b)
        self.assertEqual(a, set_type(range(100)))

    def test_method_with_set(self, set_type):
        a=set_type(range(50))
        b=set_type(range(100))
        a.update(b)
        self.assertEqual(a, set_type(range(100)))

    def test_method_with_set(self, set_type):
        a=set_type(range(50))
        b=set_type(range(100))
        a.update(b)
        self.assertEqual(a, set_type(range(100)))

    def test_method_with_iterator(self, set_type):
        a=set_type(range(50))
        a.update(range(60))
        self.assertEqual(a, set_type(range(60)))

    def test_ior(self, set_type):
        a=set_type(range(50))
        a|=set_type(range(60))
        self.assertEqual(a, set_type(range(60)))

    def test_union(self, set_type):
        a=set_type(range(30))
        a_copy = a.copy()
        b=a.union(range(30,40), set_type(range(40,50)), range(50,60))
        self.assertEqual(b, set_type(range(60)))
        self.assertEqual(a, a_copy)

    def test_union_empty(self, set_type):
        a=set_type(range(30))
        a.union()
        self.assertEqual(a, set_type(range(30)))

    def test_or(self, set_type):
        a=set_type(range(30))
        b=set_type(range(30,40))
        c=set_type(range(40,50))
        d=a|b|c
        self.assertEqual(d, set_type(range(50)))
        self.assertEqual(a, set_type(range(30)))
        self.assertEqual(b, set_type(range(30,40)))
        self.assertEqual(c, set_type(range(40,50)))


@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestSwap(UnitTestMock): 

    def test_with_none(self, set_type):
        s=set_type([1,2,3,1])
        swap=pick_fun("swap", set_type)        
        with pytest.raises(TypeError) as context:
            swap(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            swap(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            swap(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])

    def test_some_common(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([5,2,4])
        a_copy=a.copy()
        b_copy=b.copy()
        swap=pick_fun("swap", set_type) 
        swap(a,b)
        self.assertEqual(a, b_copy)
        self.assertEqual(b, a_copy)
        swap(a,b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)


@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestIntersect(UnitTestMock): 

    def test_with_none(self, set_type):
        s=set_type([1,2,3,1])
        intersect=pick_fun("intersect", set_type)        
        with pytest.raises(TypeError) as context:
            intersect(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            intersect(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            intersect(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])

    def test_small(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([5,2,4])
        a_copy=a.copy()
        b_copy=b.copy()
        intersect=pick_fun("intersect", set_type) 
        c=intersect(a,b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([2,4]))
        c=intersect(b,a)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([2,4]))

    def test_disjunct(self, set_type):
        a=set_type([1,3,5,7,9])
        b=set_type([2,2,4,6,8,10])
        a_copy=a.copy()
        b_copy=b.copy()
        intersect=pick_fun("intersect", set_type) 
        c=intersect(a,b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type())
        c=intersect(b,a)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([]))

    def test_empty(self, set_type):
        a=set_type([])
        b=set_type([])
        c=set_type([2,2,4,6,8,10])
        intersect=pick_fun("intersect", set_type) 
        d=intersect(a,b)
        self.assertEqual(len(d), 0)
        d=intersect(c,b)
        self.assertEqual(len(d), 0)
        d=intersect(a,c)
        self.assertEqual(len(d), 0)

    def test_intersection_update(self, set_type):
        a=set_type([1,2,3,4,5,6,7,8])
        b=set_type([2,4,6,8,10,12])
        b_copy = b.copy()
        a.intersection_update(b)
        self.assertEqual(a, set_type([2,4,6,8]))
        self.assertEqual(b, b_copy)

    def test_intersection_update_iter(self, set_type):
        a=set_type([1,2,3,4,5,6,7,8])
        a.intersection_update([2,4,6,8,10,12])
        self.assertEqual(a, set_type([2,4,6,8]))

    def test_empty_update(self, set_type):
        a=set_type([1,2,3,4,5,6,7,8])
        b=set_type([])
        a.intersection_update(b)
        self.assertEqual(len(a), 0)

    def test_empty_update_iter(self, set_type):
        a=set_type([1,2,3,4,5,6,7,8])
        a.intersection_update([])
        self.assertEqual(a, set_type())

    def test_iadd(self, set_type):
        a=set_type([1,2,3,4,5,6,7,8])
        b=set_type([1,104,3])
        a&=b
        self.assertEqual(a, set_type([1,3]))

    def test_add(self, set_type):
        a=set_type([1,2,3,4,5,6,7,8])
        b=set_type([1,104,3])
        a_copy=a.copy()
        b_copy=b.copy()
        c=a&b
        self.assertEqual(c, set_type([1,3]))
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)

    def test_intersection(self, set_type):
        a=set_type([1,2,3,4,5,6,7,8])
        a_copy=a.copy()
        c=a.intersection([1,2,3,4,5,6], set_type([1,2,3,4,5]), [1,2,3])
        self.assertEqual(c, set_type([1,2,3]))
        self.assertEqual(a, a_copy)


@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestDifference(UnitTestMock): 

    def test_with_none(self, set_type):
        s=set_type([1,2,3,1])
        difference=pick_fun("difference", set_type)        
        with pytest.raises(TypeError) as context:
            difference(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            difference(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            difference(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])

    def test_small(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([5,2,4])
        a_copy=a.copy()
        b_copy=b.copy()
        difference=pick_fun("difference", set_type) 
        c=difference(a,b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([1,3]))
        c=difference(b,a)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([5]))

    def test_disjunct(self, set_type):
        a=set_type([1,3,5,7,9])
        b=set_type([2,2,4,6,8,10])
        a_copy=a.copy()
        b_copy=b.copy()
        difference=pick_fun("difference", set_type) 
        c=difference(a,b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, a)
        c=difference(b,a)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, b)

    def test_empty(self, set_type):
        a=set_type([])
        b=set_type([])
        c=set_type([2,2,4,6,8,10])
        difference=pick_fun("difference", set_type) 
        d=difference(a,b)
        self.assertEqual(len(d), 0)
        d=difference(c,b)
        self.assertEqual(c, d)
        d=difference(a,c)
        self.assertEqual(len(d), 0)

    def test_method_update(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([5,2,4])
        b_copy=b.copy()
        a.difference_update(b)
        self.assertEqual(b, b_copy)
        self.assertEqual(a, set_type([1,3]))

    def test_method_update2(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([5,2,4])
        a_copy=a.copy()
        b.difference_update(a)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, set_type([5]))

    def test_method_update_from_iter(self, set_type):
        a=set_type([1,2,3,4])
        a.difference_update([5,2,4])
        self.assertEqual(a, set_type([1,3]))

    def test_method_update_from_iter2(self, set_type):
        a=set_type(range(1000))
        a.difference_update(range(0,1000,2))
        self.assertEqual(a, set_type(range(1,1000,2)))

    def test_method_update_from_iter3(self, set_type):
        a=set_type([1,2])
        a.difference_update([1]*10000)
        self.assertEqual(a, set_type([2]))

    def test_sub(self, set_type):
        a=set_type([0,222,3,444,5])
        b=set_type([222,3,4])
        a_copy=a.copy()
        b_copy=b.copy()
        c=a-b
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([0,444,5]))
        c=b-a
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([4]))

    def test_sub2(self, set_type):
        a=set_type([1,2,3,4])
        a_copy=a.copy()
        b=a-a-a-a
        self.assertEqual(a, a_copy)
        self.assertEqual(b, set_type())

    def test_isub(self, set_type):
        a=set_type([0,222,3,444,5])
        b=set_type([222,3,4])
        b_copy=b.copy()
        a-=b
        self.assertEqual(b, b_copy)
        self.assertEqual(a, set_type([0,444,5]))

    def test_isub2(self, set_type):
        a=set_type([1,2,3,4])
        a-=a
        self.assertEqual(a, set_type())


    def test_difference_method(self, set_type):
        a=set_type(range(10000))
        a_copy=a.copy()
        b=a.difference(range(5000), set_type(range(5000,10000,2)), range(1,9999,2))
        self.assertEqual(b, set_type([9999]))
        self.assertEqual(a, a_copy)


@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestSymmetricDifference(UnitTestMock): 

    def test_with_none(self, set_type):
        s=set_type([1,2,3,1])
        symmetric_difference=pick_fun("symmetric_difference", set_type)        
        with pytest.raises(TypeError) as context:
            symmetric_difference(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            symmetric_difference(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            symmetric_difference(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])

    def test_small(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([5,2,4])
        a_copy=a.copy()
        b_copy=b.copy()
        symmetric_difference=pick_fun("symmetric_difference", set_type) 
        c=symmetric_difference(a,b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([1,3,5]))
        c=symmetric_difference(b,a)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([1,3,5]))

    def test_disjunct(self, set_type):
        a=set_type([1,3,5,7,9])
        b=set_type([2,2,4,6,8,10])
        a_copy=a.copy()
        b_copy=b.copy()
        symmetric_difference=pick_fun("symmetric_difference", set_type) 
        c=symmetric_difference(a,b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, a|b)
        c=symmetric_difference(b,a)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, a|b)

    def test_empty(self, set_type):
        a=set_type([])
        b=set_type([])
        c=set_type([2,2,4,6,8,10])
        symmetric_difference=pick_fun("symmetric_difference", set_type) 
        d=symmetric_difference(a,b)
        self.assertEqual(len(d), 0)
        d=symmetric_difference(c,b)
        self.assertEqual(c, d)
        d=symmetric_difference(a,c)
        self.assertEqual(c, d)

    def test_method_update(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([5,2,4])
        b_copy=b.copy()
        a.symmetric_difference_update(b)
        self.assertEqual(b, b_copy)
        self.assertEqual(a, set_type([1,3,5]))

    def test_method_update2(self, set_type):
        a=set_type([1,2,3,4])
        b=set_type([5,2,4])
        a_copy=a.copy()
        b.symmetric_difference_update(a)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, set_type([1,3,5]))

    def test_method_update_from_iter(self, set_type):
        a=set_type([1,2,3,4])
        a.symmetric_difference_update([5,2,4])
        self.assertEqual(a, set_type([1,3, 5]))

    def test_method_update_from_iter2(self, set_type):
        a=set_type(range(1000))
        a.symmetric_difference_update(range(0,1000,2))
        self.assertEqual(a, set_type(range(1,1000,2)))

    def test_method_update_from_iter3(self, set_type):
        a=set_type([1,2])
        a.symmetric_difference_update([1]*10000)
        self.assertEqual(a, set_type([2]))


    def test_method_update_from_iter4(self, set_type):
        a=set_type([1,2])
        a.symmetric_difference_update(a)
        self.assertEqual(len(a), 0)

    def test_xor(self, set_type):
        a=set_type([0,222,3,444,5])
        b=set_type([222,3,4])
        a_copy=a.copy()
        b_copy=b.copy()
        c=a^b
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([0,444,5,4]))
        c=b^a
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)
        self.assertEqual(c, set_type([0,444,5,4]))

    def test_xor2(self, set_type):
        a=set_type([1,2,3,4])
        a_copy=a.copy()
        b=a^a^a^a
        self.assertEqual(a, a_copy)
        self.assertEqual(len(b), 0)

    def test_xor3(self, set_type):
        a=set_type([1,2,3,4])
        a_copy=a.copy()
        b=a^a^a^a^a
        self.assertEqual(a, a_copy)
        self.assertEqual(b, a)

    def test_ixor(self, set_type):
        a=set_type([0,222,3,444,5])
        b=set_type([222,3,4])
        b_copy=b.copy()
        a^=b
        self.assertEqual(b, b_copy)
        self.assertEqual(a, set_type([0,444,5,4]))

    def test_ixor2(self, set_type):
        a=set_type([1,2,3,4])
        a^=a
        self.assertEqual(a, set_type())

    def test_symmetric_method(self, set_type):
        a=set_type(range(10))
        a_copy=a.copy()
        b=a.symmetric_difference(range(5,15), set_type(range(5,10)), range(1,16))
        self.assertEqual(b, set_type([0,15]))
        self.assertEqual(a, a_copy)

