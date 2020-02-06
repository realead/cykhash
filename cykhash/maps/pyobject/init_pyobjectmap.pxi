
# see float_utils.pxi for definitions

cdef extern from *:
    """
    // preprocessor creates needed struct-type and all function definitions

    // map with keys of type pyobject -> result pyobject
    #define KHASH_MAP_INIT_PYOBJECT(name, khval_t)										\
	    KHASH_INIT(name, khpyobject_t, khval_t, 1, kh_pyobject_hash_func, kh_pyobject_hash_equal)

    //preprocessor creates needed struct-type and all function definitions 
    //set with keys of type pyobject -> resulting typename: kh_pyobjectmap_t;
    KHASH_MAP_INIT_PYOBJECT(pyobjectmap, pyobject_t)

    """
    pass


