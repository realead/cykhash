#
#
#  Attention the problem with PyObject is reference counting
#
#

cdef extern from *:
    """
    //khash has nothing predefined for Pyobject

    /*! @function
      @abstract     Instantiate a hash set containing 64-bit integer keys
      @param  name  Name of the hash table [symbol]
     */
    #define KHASH_SET_INIT_PYOBJECT(name)										\
	    KHASH_INIT(name, khpyobject_t, char, 0, kh_pyobject_hash_func, kh_pyobject_hash_equal)

    //preprocessor creates needed struct-type and all function definitions 
    //set with keys of type pyobject -> resulting typename: kh_pyobjectset_t;
    KHASH_SET_INIT_PYOBJECT(pyobjectset)

    //TODO: add generated code:
    """
    pass

