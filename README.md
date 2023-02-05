# cykhash

cython wrapper for khash-sets/maps, efficient implementation of `isin` and `unique`

## About:

  * Brings functionality of khash (https://github.com/attractivechaos/klib/blob/master/khash.h) to Python and Cython and can be used seamlessly in numpy or pandas.

  * Numpy's world is lacking the concept of a (hash-)set. This shortcoming is fixed and efficient (memory- and speedwise compared to pandas') `unique` and `isin` are implemented.

  * Python-set/dict have big memory-footprint. For some datatypes the overhead can be reduced by using khash by factor 4-8.

## Installation:

The recommended way to install the library is via `conda` package manager using the `conda-forge` channel:

    conda install -c conda-forge cykhash

You can also install the library using `pip`. To install the latest release:

    pip install cykhash

To install the most recent version of the module:

    pip install https://github.com/realead/cykhash/zipball/master

Attention: On Linux/Mac `python-dev` should be installed for that (see also https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory) and MSVC on Windows.

## Dependencies:

To build the library from source, Cython>=0.28 is required as well as a c-build tool chain.

See (https://github.com/realead/cykhash/blob/master/doc/README4DEVELOPER.md) for dependencies needed for development.

## Quick start

#### Hash set and isin

Creating a hashset and using it in `isin`:

    # prepare data:
    >>> import numpy as np 
    >>> a = np.arange(42, dtype=np.int64)
    >>> b = np.arange(84, dtype=np.int64)
    >>> result = np.empty(b.size, dtype=np.bool_)

    # actually usage
    >>> from cykhash import Int64Set_from_buffer, isin_int64

    >>> lookup = Int64Set_from_buffer(a) # create a hashset
    >>> isin_int64(b, lookup, result)    # running time O(b.size)
    >>> isin_int64(b, lookup, result)    # lookup is reused and not recreated


### `unique`

Finding `unique` in `O(n)` (compared to numpy's  `np.unique` - `O(n*logn)`) and smaller memory-footprint than pandas' `pd.unique`:

    # prepare input
    >>> import numpy as np
    >>> a = np.array([1,2,3,3,2,1], dtype=np.int64)
    
    # actual usage:
    >>> from cykhash import unique_int64
    >>> unique_buffer = unique_int64(a) # unique element are exposed via buffer-protocol

    # can be converted to a numpy-array without copying via
    >>> unique_array = np.ctypeslib.as_array(unique_buffer)
    >>> unique_array.shape
    (3,)


### Hash map

Maps and sets handle `nan`-correctly (try it out with Python's dict/set):

    >>> from cykhash import Float64toInt64Map
    >>> my_map = Float64toInt64Map() # values are 64bit integers
    >>> my_map[float("nan")] = 1
    >>> my_map[float("nan")]
    1



## Functionality overview

### Hash sets

`Int64Set`, `Int32Set`, `Float64Set`, `Float32Set` ( and `PyObjectSet`) are implemented. They are more or less drop-in replacements for Python's `set`. Furthermore, given the Cython-interface, efficient extensions of functionality are easily done.


The biggest advantage of these sets is that they need about 4-8 times less memory than the usual Python-sets and are somewhat faster for integers or floats. 

As `PyObjectSet` is somewhat slower than the usual `set` and needs about the same amount of memory, it should be used only if all `nan`s should be treated as equivalent.

The most efficient way to create such sets is to use `XXXXSet_from_buffer(...)`, e.g. `Int64Set_from_buffer`, if the data container at hand supports buffer protocol (e.g. numpy-arrays, `array.array` or `ctypes`-arrays). Or `XXXXSet_from(...)` for any iterator.


### Hash maps

`Int64toInt64Map`, `Int32toInt32Map`, `Float64toInt64Map`, `Float32toInt32Map` ( and `PyObjectMap`) are implemented. They are more or less drop-in replacements for Python's `dict` (however, not every piece of `dict`'s functionality makes sense, for example `setdefault(x, default)` without `default`-argument, because `None` cannot be inserted, also the khash-maps don't preserve the insertion order, so there is also no `reversed`). Furthermore, given the Cython-interface, efficient extensions of functionality are easily done.

Biggest advantage of these sets is that they need about 4-8 times less memory than the usual Python-dictionaries and are somewhat faster for integers or floats.


As `PyObjectMap` is somewhat slower than the usual `dict` and needs about the same amount of memory, it should be used only if all `nan`s should be treated as equivalent.

### isin

  * implemented are `isin_int64`, `isin_int32`, `isin_float64`, `isin_float32`
  * using hash set instead of arrays in `isin` function has the advantage, that the look-up data structure doesn't have to be reconstructed for every call, thus reducing the running time from `O(n+m)`to `O(n)`, where `n` is the number of queries and `m`-number of elements in the look up array.
  * Thus cykash's `isin` can be order of magnitude faster than the numpy's or pandas' versions.

#### all, none, any, and count_if

  * siblings functions of `isin_XXX` are:
      * `all_XXX`/`all_XXX_from_iterator` which return `True` if all elements of the query array can be found in the set.
      * `any_XXX`/`any_XXX_from_iterator` which return `True` if at least one element of the query array can be found in the set.
      * `none_XXX`/`none_XXX_from_iterator` which return `True` if none of  elements from the query array can be found in the set.
      * `count_if_XXX`/`count_if_XXX_from_iterator` which return the number of elements from the query array can be found in the set.
  * `all_XXX`, `any_XXX`, `none_XXX` and `count_if_XXX` are faster than using `isin_XXX` and applying numpy's versions of these function on the resulting array.
  * `from_iterator` version works with any iterable, but the version for buffers are more efficient.

### unique

  * implemented are `unique_int64`, `unique_int32`, `unique_float64`, `unique_float32`
  * returns an object which implements the buffer protocol, so `np.ctypeslib.as_array` (recommended) or `np.frombuffer` (less safe, as memory can get reinterpreted) can be used to create numpy arrays.
  * differently as pandas, the returned uniques aren't in the order of the appearance. If order of appearence is important use `unique_stable_xxx`-versions, which needs somewhat more memory.
  * the signature is `unique_xxx(buffer, size_hint=0.0)` the initial memory-consumption of the hash-set will be `len(buffer)*size_hint` unless `size_hint<=0.0`, in this case it will be ensured, that no rehashing is needed even if all elements are unique in the buffer.

As pandas uses maps instead of sets internally for `unique`, it needs about 4 times more peak memory and is 1.6-3 times slower.


### Floating-point numbers as keys

There is a problem with floating-point sets or maps, i.e. `Float64Set`, `Float32Set`, `Float64toInt64Map` and `Float32toInt32Map`: The standard definition of "equal" and hash-function based on the bit representation don't define a meaningful or desired behavior for the hash set:

   * `NAN != NAN` and thus it is not equivalence relation
   * `-0.0 == 0.0` but `hash(-0.0)!=hash(0.0)`, but `x==y => hash(x)==hash(y)` is neccessary for set to work properly.

This problem is resolved through following special case handling:

   * `hash(-0.0):=hash(0.0)`
   * `hash(x):=hash(NAN)` for any not a number `x`.
   * `x is equal y <=> x==y || (x!=x && y!=y)`

A consequence of the above rule, that the equivalence classes of `{0.0, -0.0}` and `e{x | x is not a number}` have more than one element. In the set these classes are represented by the first seen element from the class.

The above holds also for `PyObjectSet` (this behavior is not the same as fro Python-`set` which shows a different behavior for nans).

### Examples:

#### Hash sets

Python: Creates a set from a numpy-array and looks up whether an element is in the resulting set:

    >>> import numpy as np
    >>> from cykhash import Int64Set_from_buffer
    >>> a =  np.arange(42, dtype=np.int64)
    >>> my_set = Int64Set_from_buffer(a) # no reallocation will be needed
    >>> 41 in my_set 
    True
    >>> 42 not in my_set
    True

Python: Create a set from an iterable and looks up whether an element is in the resulting set:

    >>> from cykhash import Int64Set_from
    >>> my_set = Int64Set_from(range(42)) # no reallocation will be needed
    >>> assert 41 in my_set and 42 not in my_set

Cython: Create a set and put some values into it:

    from cykhash.khashsets cimport Int64Set
    my_set = Int64Set(number_of_elements_hint=12)  # reserve place for at least 12 integers
    cdef Py_ssize_t i
    for i in range(12):
       my_set.add(i)
    assert 11 in my_set and 12 not in my_set

#### Hash maps

Python: Creating `int64->float64` map using `Int64toFloat64Map_from_buffers`:

    >>> import numpy as np
    >>> from cykhash import Int64toFloat64Map_from_buffers
    >>> keys = np.array([1, 2, 3, 4], dtype=np.int64)
    >>> vals = np.array([5, 6, 7, 8], dtype=np.float64)
    >>> my_map = Int64toFloat64Map_from_buffers(keys, vals) # there will be no reallocation
    >>> assert my_map[4] == 8.0

Python: Creating `int64->int64` map from scratch:

    >>> import numpy as np
    >>> from cykhash import Int64toInt64Map

    # my_map will not need reallocation for at least 12 elements
    >>> my_map = Int64toInt64Map(number_of_elements_hint=12)
    >>> for i in range(12):  my_map[i] = i+1
    >>> assert my_map[5] == 6


#### isin

Python: Creating look-up data structure from a numpy-array, performing `isin`-query

    >>> import numpy as np
    >>> from cykhash import Int64Set_from_buffer, isin_int64
    >>> a = np.arange(42, dtype=np.int64)
    >>> lookup = Int64Set_from_buffer(a)

    >>> b = np.arange(84, dtype=np.int64)
    >>> result = np.empty(b.size, dtype=np.bool_)

    >>> isin_int64(b, lookup, result)    # running time O(b.size)
    >>> assert np.sum(result.astype(np.int_)) == 42


#### unique

Python: using `unique_int64`:

    >>> import numpy as np
    >>> from cykhash import unique_int64
    >>> a = np.array([1,2,3,3,2,1], dtype=np.int64)
    >>> u = np.ctypeslib.as_array(unique_int64(a)) # there will be no reallocation
    >>> assert set(u) == {1,2,3}

Python: using `unique_stable_int64`: 

    >>> import numpy as np
    >>> from cykhash import unique_stable_int64
    >>> a = np.array([3,2,1,1,2,3], dtype=np.int64)
    >>> u = np.ctypeslib.as_array(unique_stable_int64(a)) # there will be no reallocation
    >>> assert list(u) == [3,2,1] 



## API

See (https://github.com/realead/cykhash/blob/master/doc/README_API.md) for a more detailed API description.

## Performance

See (https://github.com/realead/cykhash/blob/master/doc/README_PERFORMANCE.md) for results of performance tests.

## Trivia

* This project was inspired by the following stackoverflow question: https://stackoverflow.com/questions/50779617/pandas-pd-series-isin-performance-with-set-versus-array.

* pandas also uses `khash` (and thus was a source of inspiration), but wraps only maps and doesn't wrap sets. Thus, pandas' `unique` needs more memory as it should. Those maps are also never exposed, so there is no way to reuse the look-up structure for multiple calls to `isin`.

* `khash` is a good choice, but there are other alternatives, e.g. https://github.com/sparsehash/sparsehash. See also https://stackoverflow.com/questions/48129713/fastest-way-to-find-all-unique-elements-in-an-array-with-cython/48142655#48142655 for a comparison for different `unique` implementations.

* A similar approach for sets/maps in pure Cython: https://github.com/realead/tighthash, which is quite slower than khash.

* There is no dependency on `numpy`: this library uses buffer protocol, thus it works for `array.array`, `numpy.ndarray`, `ctypes`-arrays and anything else. However, some interfaces are somewhat cumbersome (which type should be created as answer?) and for convenient usage it might be a good idea to wrap the functionality so objects of right types are created.

## Compatibility between cykhash-versions:

There are different levels of compatibility: 

 * for code using only pure python interface
 * for code using cython/cdef-interface and built against a particular cykash version

Ther rules are as follows:
 
 * there is no warranty for major versions mismatch: i.e. code written with cykhash `1.x.y` might not run with cykhash `2.z.w` and vice versa.
 * if only pure python interface is used, code for the same major version will ran for version with higher minor version, i.e. code for cykhash `2.0.x` will run with cykhash `2.1.y` (but not the other way around: that means new functions could be added to pure python interface)
 * if cython's `cdef` interface is used, i.e. a cython-extension was build using pxi-files from cykhash, then versions are compartible only if the the minor versions are the same, e.g. `2.0.x` could be replaced by `2.0.y` in the installation, but when replacing with `2.1.z` the dependent cython-extension must be rebuilt.

## History:
### Release 2.0.1 (05.02.2022):

  * Tests work for Python 3.11
  * Tests work for numpy 1.24
  * Drops support for Python 3.6 and Python 3.7

#### Release 2.0.0 (09.11.2021):

  * Implementation of `any`, `all`, `none` and `count_if`
  * Hash-sets are now (almost) drop-in replacements of Python's sets
  * Breaking change: iterator from maps doesn't no longer returns items but only keys. However there are following new methods `keys()`, `values()` and `items()`which return so called mapvies, which correspond more or less to dictviews (but for mapsview doesn't hold that "Dictionary order is guaranteed to be insertion order.").
  * Hash-Maps are now (almost) drop-in replacements of Python's dicts. Differences: insertion order isn't preserved, thus there is also no `reversed()`-method, `setdefault(key, default)` isn't possible without `default` because `None` cannot be inserted in the map
  * Better hash-functions for float64, float32, int64 and int32 (gh-issue #4).
  * Breaking change: different names/signatures for maps
  * supports tracemalloc for Py3.6+
  * supports Python 3.10

#### Release 1.0.2 (30.05.2020):

  * can be installed via conda-forge to all operating systems
  * can be installed via pip in a clean environment (Cython>=0.28 is now fetched automatically)

#### Release 1.0.1 (27.05.2020):

  * released on PyPi

#### Older:

  * 0.4.0: uniques_stable, preparing for release
  * 0.3.0: PyObjectSet, Maps for Int64/32 and also Float64/32, unique-versions
  * 0.2.0: Int32Set, Float64Set, Float32Set
  * 0.1.0: Int64Set

