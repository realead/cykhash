from unittestmock import UnitTestMock
import pytest

from cykhash import Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet

@pytest.mark.parametrize(
    "set_type",
    [Int64Set, Int32Set, Float64Set, Float32Set, PyObjectSet]
)
class TestSetIterator(UnitTestMock): 

    def test_iterate(self, set_type):
        cy_set = set_type()
        py_set = set()
        for i in range(10):
         cy_set.add(i)
         py_set.add(i)
        clone = set()
        for x in cy_set:
         clone.add(x)
        self.assertEqual(py_set, clone)

    def test_iterate_after_clear(self, set_type):
        cy_set = set_type(range(1000))
        it = iter(cy_set)
        for x in range(1000):
            next(it)
        cy_set.clear()
        with pytest.raises(StopIteration):
            next(it)

    def test_iterate_after_growing(self, set_type):
        cy_set = set_type()
        it = iter(cy_set)
        #change bucket size
        for i in range(1000):
            cy_set.add(i)
        #make sure new size is used
        lst = []
        with pytest.raises(StopIteration):
            for x in range(1001):
                lst.append(next(it))
        self.assertEqual(set(lst), set(range(1000)))

    def test_iterate_after_growing2(self, set_type):
        cy_set = set_type()
        cy_set.add(42)
        it = iter(cy_set)
        next(it) #iterator shows to end now
        cy_set.add(11)
        cy_set.add(15)
        cy_set.add(13)
        #old end is no longer an end
        try:
            self.assertTrue(next(it) in {42,11,15,13})
        except StopIteration:
            pass # stop iteration could be an acceptable outcome

