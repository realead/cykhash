from unittestmock import UnitTestMock
import pytest

from cykhash import Int64toInt64Map, Int32toInt32Map, Float64toInt64Map, Float32toInt32Map, PyObjectMap
from cykhash import Int64toFloat64Map, Int32toFloat32Map, Float64toFloat64Map, Float32toFloat32Map
import cykhash

nopython_maps = [Int64toInt64Map, Int32toInt32Map, Float64toInt64Map, Float32toInt32Map,
                 Int64toFloat64Map, Int32toFloat32Map, Float64toFloat64Map, Float32toFloat32Map]
all_maps = nopython_maps + [PyObjectMap]

SUFFIX={Int64toInt64Map : "int64toint64map",  
        Int32toInt32Map : "int32toint32map",  
        Float64toInt64Map : "float64toint64map",  
        Float32toInt32Map : "float32toint32map", 
        Int64toFloat64Map : "int64tofloat64map",  
        Int32toFloat32Map : "int32tofloat32map",  
        Float64toFloat64Map : "float64tofloat64map",  
        Float32toFloat32Map : "float32tofloat32map",  
        PyObjectMap : "pyobjectmap"}
def pick_fun(name, map_type):
    return getattr(cykhash, name+"_"+SUFFIX[map_type])


@pytest.mark.parametrize(
    "map_type",
    all_maps
)
class TestMapDropin(UnitTestMock): 
    def test_init_int_from_iter(self, map_type):
        m=map_type([(1,2),(3,1)])
        self.assertEqual(len(m), 2)
        self.assertEqual(m[1],2)
        self.assertEqual(m[3],1)

    def test_fromkeys(self, map_type):
        m=map_type.fromkeys([1,2,3], 55)
        self.assertEqual(len(m), 3)
        self.assertEqual(m[1],55)
        self.assertEqual(m[2],55)
        self.assertEqual(m[3],55)

    def test_clear(self, map_type):
        a=map_type([(1,2), (2,3)])      
        a.clear()
        self.assertEqual(len(a), 0)
        a[5]=6
        self.assertEqual(a[5], 6)
        a.clear()
        self.assertEqual(len(a), 0)

    def test_iterable(self, map_type):
        a=map_type([(1,4), (2,3)])      
        keys = list(a)
        self.assertEqual(set(keys), {1,2})

    def test_setintem_getitem_delitem(self, map_type):
        a=map_type()      
        a[5] = 42
        self.assertEqual(len(a), 1)
        self.assertTrue(a)
        self.assertEqual(a[5], 42)
        del a[5]
        self.assertEqual(len(a), 0)
        self.assertFalse(a)
        with pytest.raises(KeyError) as context:
            a[5]
        self.assertEqual(context.value.args[0], 5)
        with pytest.raises(KeyError) as context:
            a[5]
        self.assertEqual(context.value.args[0], 5)

    def test_get(self, map_type):
        a=map_type([(1,2)])
        self.assertEqual(a.get(1), 2)
        self.assertTrue(a.get(2) is None)
        self.assertEqual(a.get(1, 5), 2)
        self.assertEqual(a.get(2, 5), 5)      
        with pytest.raises(TypeError) as context:
            a.get(1,2,4)
        self.assertEqual("get() expected at most 2 arguments, got 3", context.value.args[0])
        with pytest.raises(TypeError) as context:
            a.get(1,default=9)
        self.assertEqual("get() takes no keyword arguments", context.value.args[0])
        with pytest.raises(TypeError) as context:
            a.get()
        self.assertEqual("get() expected at least 1 arguments, got 0", context.value.args[0])

    def test_pop(self, map_type):
        a=map_type([(1,2)])
        self.assertTrue(a.pop(2, None) is None)
        self.assertEqual(a.pop(1, 5), 2)
        self.assertEqual(len(a), 0)
        self.assertEqual(a.pop(1, 5), 5)
        self.assertEqual(a.pop(2, 5), 5)
        with pytest.raises(KeyError) as context:
            a.pop(1)
        self.assertEqual(1, context.value.args[0])      
        with pytest.raises(TypeError) as context:
            a.pop(1,2,4)
        self.assertEqual("pop() expected at most 2 arguments, got 3", context.value.args[0])
        with pytest.raises(TypeError) as context:
            a.pop(1,default=9)
        self.assertEqual("pop() takes no keyword arguments", context.value.args[0])
        with pytest.raises(TypeError) as context:
            a.pop()
        self.assertEqual("pop() expected at least 1 arguments, got 0", context.value.args[0])

    def test_popitem(self, map_type):
        a=map_type([(1,2)])
        self.assertEqual(a.popitem(), (1,2))
        self.assertEqual(len(a), 0)
        with pytest.raises(KeyError) as context:
            a.popitem()
        self.assertEqual("popitem(): dictionary is empty", context.value.args[0])     

    def test_popitem2(self, map_type):
        a=map_type(zip(range(1000), range(1000)))
        s=set()
        for i in range(1000):
            s.add(a.popitem())
        self.assertEqual(len(a), 0)
        self.assertEqual(s, set(zip(range(1000), range(1000))))

    def test_setdefault(self, map_type):
        a=map_type()
        self.assertEqual(a.setdefault(2,4), 4)
        self.assertEqual(a.setdefault(2,5), 4)
        self.assertEqual(len(a), 1)
        self.assertEqual(a[2], 4)
        self.assertEqual(a.setdefault(4,4444), 4444)
        self.assertEqual(len(a), 2)



@pytest.mark.parametrize(
    "map_type",
    all_maps
)
class TestSwap(UnitTestMock): 
    def test_with_none(self, map_type):
        swap=pick_fun("swap", map_type)
        a=map_type([(1,2),(3,1)])
        with pytest.raises(TypeError) as context:
            swap(None,a)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            swap(a,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            swap(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])


    def test_swap(self, map_type):
        swap=pick_fun("swap", map_type)
        a=map_type([(1,2),(3,1),(5,3)])
        b=map_type([(2,3),(4,6)])
        swap(a,b)
        self.assertEqual(len(a), 2)
        self.assertEqual(a[2], 3)
        self.assertEqual(a[4], 6)
        self.assertEqual(len(b), 3)
        self.assertEqual(b[1], 2)
        self.assertEqual(b[3], 1)
        self.assertEqual(b[5], 3)

    def test_empty(self, map_type):
        swap=pick_fun("swap", map_type)
        a=map_type(zip(range(1000), range(1000)))
        b=map_type()
        swap(a,b)
        self.assertEqual(len(a), 0)
        self.assertEqual(len(b), 1000)
        a[6]=3
        self.assertEqual(len(a), 1)
        b[1000]=0
        self.assertEqual(len(b), 1001)



@pytest.mark.parametrize(
    "map_type",
    all_maps
)
class TestDictView(UnitTestMock): 
    def test_len(self, map_type):
        a=map_type([(1,2),(3,1),(5,3)])
        self.assertEqual(len(a.keys()), 3)
        self.assertEqual(len(a.items()), 3)
        self.assertEqual(len(a.values()), 3)

    def test_in(self, map_type):
        a=map_type([(1,2),(3,1),(5,3)])
        self.assertEqual(5 in a.keys(), True)
        self.assertEqual(6 in a.keys(), False)
        self.assertEqual(2 in a.values(), True)
        self.assertEqual(6 in a.values(), False)
        self.assertEqual((3,1) in a.items(), True)
        self.assertEqual((5,5) in a.items(), False)


@pytest.mark.parametrize(
    "map_type",
    all_maps
)
class TestAreEqual(UnitTestMock): 

    def test_with_none(self, map_type):
        s=map_type([(1,1),(2,2),(3,3),(1,1)])
        are_equal=pick_fun("are_equal", map_type)
        with pytest.raises(TypeError) as context:
            are_equal(None,s)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            are_equal(s,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            are_equal(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])

    def test_with_empty(self, map_type):
        a=map_type()
        b=map_type()
        are_equal=pick_fun("are_equal", map_type)
        self.assertEqual(are_equal(a,b), True)
        self.assertEqual(are_equal(b,a), True)
        self.assertEqual(a==b, True)
        self.assertEqual(b==a, True)

    def test_with_one_empty(self, map_type):
        a=map_type([(1,2)])
        b=map_type()
        are_equal=pick_fun("are_equal", map_type)
        self.assertEqual(are_equal(a,b), False)
        self.assertEqual(are_equal(b,a), False)
        self.assertEqual(a==b, False)
        self.assertEqual(b==a, False)


    def test_small_yes(self, map_type):
        a=map_type([(1,2), (3,4)])
        b=map_type([(3,4), (1,2)])
        are_equal=pick_fun("are_equal", map_type)
        self.assertEqual(are_equal(a,b), True)
        self.assertEqual(are_equal(b,a), True)
        self.assertEqual(a==b, True)
        self.assertEqual(b==a, True)

    def test_small_no(self, map_type):
        a=map_type([(1,2), (3,4)])
        b=map_type([(3,4), (2,2)])
        are_equal=pick_fun("are_equal", map_type)
        self.assertEqual(are_equal(a,b), False)
        self.assertEqual(are_equal(b,a), False)
        self.assertEqual(a==b, False)
        self.assertEqual(b==a, False)

    def test_small_no_diffsizes(self, map_type):
        a=map_type([(1,2), (3,4), (3,4)])
        b=map_type([(3,4), (2,2), (3,3)])
        are_equal=pick_fun("are_equal", map_type)
        self.assertEqual(are_equal(a,b), False)
        self.assertEqual(are_equal(b,a), False)
        self.assertEqual(a==b, False)
        self.assertEqual(b==a, False)

    def test_large_method(self, map_type):
        a=map_type(zip(range(33,10000,3), range(33,10000,3)))
        b=map_type(zip(range(33,10000,3), range(33,10000,3)))
        are_equal=pick_fun("are_equal", map_type)
        self.assertEqual(are_equal(a,b), True)
        self.assertEqual(are_equal(b,a), True)
        self.assertEqual(a==b, True)
        self.assertEqual(b==a, True)


@pytest.mark.parametrize(
    "map_type",
    all_maps
)
class TestCopy(UnitTestMock): 

    def test_with_none(self, map_type):
        copy=pick_fun("copy", map_type)
        self.assertTrue(copy(None) is None)

    def test_with_empty(self, map_type):
        a=map_type([])
        copy=pick_fun("copy", map_type)
        self.assertEqual(len(copy(a)), 0)

    def test_small(self, map_type):
        a=map_type([(1,1),(2,2),(3,3),(1,1)])
        copy=pick_fun("copy", map_type)
        self.assertEqual(copy(a)==a, True)

    def test_large(self, map_type):
        a=map_type(zip(range(33,10000,3), range(33,10000,3)))
        copy=pick_fun("copy", map_type)
        self.assertEqual(copy(a)==a, True)

    def test_large_method(self, map_type):
        a=map_type(zip(range(33,10000,3), range(33,10000,3)))
        self.assertEqual(a.copy()==a, True)


@pytest.mark.parametrize(
    "map_type",
    all_maps
)
class TestUpdate(UnitTestMock): 
    def test_with_none(self, map_type):
        update=pick_fun("update", map_type)
        a=map_type([(1,2),(3,1)])
        with pytest.raises(TypeError) as context:
            update(None,a)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            update(a,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])
        with pytest.raises(TypeError) as context:
            update(None,None)
        self.assertTrue("'NoneType' object is not iterable" in context.value.args[0])


    def test_update(self, map_type):
        update=pick_fun("update", map_type)
        a=map_type([(1,2),(3,1)])
        b=map_type([(1,3),(4,6)])
        b_copy=b.copy()
        update(a,b)
        self.assertEqual(a, map_type([(1,3), (3,1), (4,6)]))
        self.assertEqual(b, b_copy)

    def test_update_empty(self, map_type):
        update=pick_fun("update", map_type)
        a=map_type([(1,2),(3,1)])
        a_copy=a.copy()
        b=map_type([])
        update(a,b)
        self.assertEqual(a, a_copy)
        self.assertEqual(len(b), 0)
        update(b,a)
        self.assertEqual(b, a_copy)
        self.assertEqual(a, a_copy)

    def test_update_large(self, map_type):
        update=pick_fun("update", map_type)
        a=map_type(zip(range(1000), range(1,995)))
        b=map_type(zip(range(2000), range(2000)))
        update(a,b)
        self.assertEqual(a, b)

    def test_update_method(self, map_type):
        a=map_type([(1,2),(3,1)])
        b=map_type([(1,3),(4,6)])
        b_copy=b.copy()
        a.update(b)
        self.assertEqual(a, map_type([(1,3), (3,1), (4,6)]))
        self.assertEqual(b, b_copy)

    def test_update_from_iter(self, map_type):
        a=map_type([(1,2),(3,1)])
        a.update([(1,3),(4,6)])
        self.assertEqual(a, map_type([(1,3), (3,1), (4,6)]))

    def test_update_from_wrong_iter(self, map_type):
        a=map_type([(1,2),(3,1)])
        with pytest.raises(ValueError) as context:
            a.update([(1,3),(4,6,4)])
        self.assertEqual("too many values to unpack (expected 2)", context.value.args[0])
        with pytest.raises(ValueError) as context:
            a.update([(1,3),(4,)])
        self.assertEqual("need more than 1 value to unpack", context.value.args[0])



   



