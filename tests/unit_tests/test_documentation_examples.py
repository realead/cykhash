import unittest


class DocTester(unittest.TestCase): 

    def test_create_set_from_buffer(self):
        import numpy as np
        from cykhash import Int64Set_from_buffer       
        a =  np.arange(42, dtype=np.int64)
        my_set = Int64Set_from_buffer(a) # no reallocation will be needed
        assert 41 in my_set and 42 not in my_set

        self.assertTrue(True)


    def test_create_set_from_iterator(self):
        from cykhash import Int64Set_from
        my_set = Int64Set_from(range(42)) # no reallocation will be needed
        assert 41 in my_set and 42 not in my_set

        self.assertTrue(True)


    def test_is_in(self):
        import numpy as np
        from cykhash import Int64Set_from_buffer, isin_int64
        a = np.arange(42, dtype=np.int64)
        lookup = Int64Set_from_buffer(a)

        b = np.arange(84, dtype=np.int64)
        result = np.empty(b.size, dtype=np.bool)

        isin_int64(b, lookup, result)
        assert np.sum(result.astype(np.int))==42

        self.assertTrue(True)


    def test_unique(self):
        import numpy as np
        from cykhash import unique_int64
        a = np.array([1,2,3,3,2,1], dtype=np.int64)
        u = np.ctypeslib.as_array(unique_int64(a)) # there will be no reallocation
        print(u) # [1,2,3] or any permutation of it

        self.assertTrue(True)


    def test_stable_unique(self):
        import numpy as np
        from cykhash import unique_stable_int64
        a = np.array([3,2,1,1,2,3], dtype=np.int64)
        u = np.ctypeslib.as_array(unique_stable_int64(a)) # there will be no reallocation
        print(u) # [3,2,1] 

        self.assertTrue(True)


    def test_int64map_from_buffer(self):
        import numpy as np
        from cykhash import Int64to64Map_from_float64_buffer
        keys = np.array([1, 2, 3, 4], dtype=np.int64)
        vals = np.array([5, 6, 7, 8], dtype=np.float64)
        my_map = Int64to64Map_from_float64_buffer(keys, vals) # there will be no reallocation
        assert my_map[4] == 8.0

        self.assertTrue(True)


    def test_int64map_from_scrarch(self):
        import numpy as np
        from cykhash import Int64to64Map
        # my_map will not need reallocation for at least 12 elements and
        # values are int64 (another possibility is for_int=False, meas for float64
        my_map = Int64to64Map(number_of_elements_hint=12, for_int=True)
        for i in range(12):
            my_map[i] = i+1
        assert my_map[5] == 6

        self.assertTrue(True)

        
    
