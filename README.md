# cykhash

cython wrapper for khash

## About:

  * Brings functionality of khash (https://github.com/attractivechaos/klib/blob/master/khash.h) to Cython and can be used seamlessly in numpy or pandas.

  * Numpy's world is lacking the concept of a (hash-)set. This shortcoming is fixed and thus efficient `unique` and `isin` implementations are possible.

  * Python-set has a big memory-footprint. For some datatypes the overhead can be reduced by using khash.

  * Is inspired by usage of khash in pandas.
  
  * For python3 (versions 0.1 and 0.2 supported also python2)

This project was inspired by the following stackoverflow question: https://stackoverflow.com/questions/50779617/pandas-pd-series-isin-performance-with-set-versus-array

## Dependencies:

Essential:

  * Cython>=0.28 because verbatim C-code feature is used
  * build tool chain (for example gcc on Linux)

Additional dependencies for testing:

  * `sh`
  * `virtualenv`
  * `uttemplate`>=0.2.0 (https://github.com/realead/uttemplate)
  * `numpy`, `pandas`, `perfplot` for performance tests

## Instalation:

To install the module using pip run:

    pip install https://github.com/realead/cykhash/zipball/master

It is possible to uninstall it afterwards via

    pip uninstall cykhash

You can also install using the `setup.py` file from the root directory of the project:

    python setup.py install

However, there is no easy way to deinstall it afterwards (only manually) if `setup.py` was used directly.

## Performance

Run `sh run_perf_tests.sh` in tests-folder to reproduce. numpy and pandas will be installed in addtion to be able to run the performance tests. The easiest way is to call first `sh test_instalation.sh p3 local keep` and than activate it via `. ../p3/bin/activate` and only then call the performance 

#### Memory consumption:

Peak memory usage for N int64-integers (inclusive python-interpreter):

                      10^3       10^4      10^5       10^6      10^7
    python2-set        6MB        6MB      13MB       62MB      502MB
    python3-set        8MB        9MB      17MB       79MB      588MB
    cykhash (p3)      10MB       10MB      10MB       26MB      147MB

i.e. there is about 4 time less memory needed.


#### pd.unique()

Warning: cykhash's version of `unique` doesn't not return uniques in order of appearance (which pandas' version does!). `cykhash.unique` returns a object with buffer-interface, which can be used for creation of numpy-arrays via `np.frombuffer`.

The implementation of pandas' `unique` uses a hash-table instead of hash-set, which results in a larger memory footprint. `cykhash.unique_int64` (or `unique_int32`, `unique_float32`, `unique_float64`) uses much less memory and is also faster. See also question https://stackoverflow.com/questions/51485816/curious-memory-consumption-of-pandas-unique for more details.


![1](imgs/unique_time_comparison.png)

There is no int32-version in `pandas`, such there is no difference to 64bit. `int32`-version of `cykhash` is twice as fast as `int64`-version, which is about factor 1.66 faster than the pandas' version. Run `tests/perf_tests/khashunique_vs_pdunique.py` to generate the plot.

Peak memory overhead (additional needed memory given as `maximal_overhead_factor`) for unique (run `tests/perf_tests/run_memory_unique_test.sh` to generate the numbers). i.e. additional memory needed is `N*maximal_overhead_factor`


    N      pd.unique()   cykhash.unique_int64
    1e6        6.24          2.18
    2e6        6.19          2.15
    4e6        6.35          2.16
    6e6        4.86          1.44
    8e6        6.25          2.16
    9e6        7.50          1.90

While `pd.unique` needs up to 8 times the original memory, `cykhash` at most 3 times the original memory. For the special case of `int32` the overhead-factor of `pd.unique` more than doubles because it doesn't have a dedicated int32-version and data must be converted to int64. 

More precise the worst case scenario (while still without triggering rehashing) for `cykhash.unique_int64`, the overhead-factor can be `1.3*2*(1+1/64)=2.64` where:
  
 * 1.3 due to the fact that rehashing happens when more than 77% of buckets are occupied.
 * 2 due to the fact, that khash doubles the size every time
 * 1+1/64 that one bit is used for flags



#### isin

Compared to pandas' `isin`, which has a linear running time in number of elements in the lookup. cykhash's `isin` has a `O(1)` in the number of elements in the look-up:

    n	pandas(#look-up=10^n)	cykhash(#look-up=10^n)
    2 	 0.0009466878400417045 	 0.0008094332498149015
    3 	 0.0011027359400759451 	 0.001505808719957713
    4 	 0.001315673690114636 	 0.0005093092197785154
    5 	 0.007601776499941479 	 0.00031931002013152465
    6 	 0.11544147745007649 	 0.000292295379913412
    7 	 0.7747500354002114 	 0.00047073251014808195

#### PyObjectSet:

There are no advantages (others that nans are handled correctly, more about it later) to use khash-version for normal Python-objects.

One caveau: `PyObject_Hash` doesn't yield a good hash-function (for example for integer `k` it is `k` and using it leads to quite bad results (running `python tests/perf_tests/pyobjectset_vs_set.py`):

![1](imgs/set_vs_pyobjectset.png)

as one can see, it is about 50 times slower then Python-set, and seems to have worse than linear behavior.

The problem is the "discard"  part, as the insertions alone aren't problematic:


![1](imgs/set_vs_pyobjectset_only_insert.png)

Fixing it, leads to somewhat better discard behavior:


![2](imgs/set_vs_pyobjectset_fixed_hash.png)

It is only 2 times slower than Python-set for inserting elements (but still somewhat not quite linear?. However it has also a negative impact on `insert`:

![1](imgs/set_vs_pyobjectset_only_insert_fixed_hash.png)


As conclusion:

   * `contains` are almost equally fast for `set`/`PyObjectSet`.
   * `insert` is slightly slower for `PyObjectSet`, preallocation should be used whenever possible.
   * `discard` is quite slow for `PyObjectSet`.


Insertion of Python-integers is 50% slower than the insertion of 64bit integers (see `tests/perf_tests/object_vs_int64_via_buffer.py`):

![1](imgs/buffer_objects_int64.png)

Using `PyObjectSet_from_buffer` is about 2.5 times faster than from iterator and 3 times faster than using `add`.

For best performance use `Int64Set` or, even better, `Int32Set`, which is about factor 2 faster than the 64bit-version.

 
#### PyObjectMap:

There are similar observation as for `PyObjectMap`, see `map_object_vs_int64_via_buffer.py` and `pyobjectmap_vs_dict.py` in 'tests/perf_tests`-folder.

The results are slightly worse (all above discard):

![1](imgs/map_vs_pyobjectmap_fixed_hash.png)

and

![1](imgs/map_vs_pyobjectmap_only_insert_fixed_hash.png)

Also here the performance of the 64bit/32bit variant much better:


![1](imgs/buffer_objects_int64_map.png)


## Usage:

### Unique

  * `unique_int64`, `unique_int32`, `unique_float64`, `unique_float32`
  * returns an object which implements the buffer protocol, so `np.ctypeslib.as_array` (recommended) or `np.frombuffer` (less safe, as memory can get reinterpreted) can be used to create numpy arrays.
  * differently as pandas, the returned uniques aren't in the order of the appearance.

### Sets

Following classes are defined: 
         
  * `Int64Set` for 64 bit integers
  * `Int32Set` for 32 bit integers
  * `Float64Set`for 64 bit floats 
  * `Float32Set`for 32 bit floats 
  * `PyObjectSet`for arbitrary Python-objects

with Python interface:

  * `__len__`: number of elements in the set
  * `__contains__`: whether an element is contained in the set
  * `add`: adds an element to set
  * `discard`: remove an element or do nothing if element is not in the set
  * `__iter__`: returns an iterator through all elements in set

with Cython interface:

  * `contains`: checks whether an element is contained in the set
  * `add` : adds an element to the set
  * `discard` : remove an element or do nothing if element is not in the set
  * `get_iter`: returns an iterator with the following Cython interface:
       * `has_next`:returns true if there are more elements in the iterator
       * `next` :returns next element and moves the iterator

### Utility functions:

The following functions are available:

   * `XXXXSet_from(it)` - creates a `XXXXSet` from an iterable, with `XXXX` being either `Int64`, `Int32`, `Float64`, `Float32` or `PyObject`.
   * `XXXXSet_from_buffer(buf, size_hint=1.25)` creates a `XXXXSet` from an object which implements buffer interface, with `XXXX` being either `Int64`, `Int32`, `Float64`, `Float32` or `PyObject`. Starting size of hash-set is `int(size_hint*len(buf))`.
  * `isin_xxxx(query, db, result)` evaluates `isin` for `query` being a buffer of the right type, `db` - a corresponding `XXXXSet`, and result a buffer for with 8bit-itemsize, `xxxx` being either `int64`, `int32`, `float64`, `float32` or `pyobject`.


### Maps

Following classes are defined: 
         
  * `Int64to64Map` for mapping  64 bit integers to 64bit integer/floats
  * `Int32to32Map` for mapping 32 bit integers to 32bit integer/floats
  * `Float64to64Map`for mapping 64 bit floats to 64bit integer/floats
  * `Float32to32Map`for mapping 32 bit floats to 32bit integer/floats
  * `PyObjectMap`for arbitrary Python-objects as key/values

with Python interface:

  * `__len__`: number of elements in the map
  * `__contains__`: whether an element is contained in the map
  * `put_XXint/get_XXint`: setting/retrieving elements with XX=32 or 64 bits integer 
  * `put_XXfloat/get_XXfloat`: setting/retrieving elements with XX=32 or 64 bits float 
  * `__setitem__/__getitem___`: parameter `for_intXX` in the constructor deceides whether elements are intepreted as int or float (XX =  32 or 64 bits)
  * `discard`: remove an element or do nothing if element is not in the map
  * `__iter__`: returns an iterator through all elements in map

with Cython interface:

  * `contains`: checks whether an element is contained in the map
  * `put_XXint/get_XXint,put_XXfloat/get_XXfloat` : setting/getting elements in the map
  * `discard` : remove an element or do nothing if element is not in the map
  * `get_iter`: returns an iterator with the following Cython interface:
       * `has_next`:returns true if there are more elements in the iterator
       * `next` :returns next element and moves the iterator

### Utility functions:

The following functions are available:

   * `TypeXXtoXXMap_from_typeXX_buffer(keys, vals, size_hint)` - creates a `TypeXXtoXXMyp` from buffers with  `Type` either `Float` or `Int`, `XX` either 32 or 64 and `type` either `float` or `int`. Starting size of hash-map is `int(size_hint*min(len(keys), len(vals)))`.
   * `PyObjectMap_from_object_buffer` for keys, values as objects.

### Examples: 

In pure python:
 
    from cykhash import Int64Set
    s=Int64Set()
    s.add(1)
    print(1 in s)#prints true

In Cython:

    from cykhash.khashsets cimport Int64Set

    #returns True/False if element in db/not
    def isin(query, Int64Set db):
        for i in query:
            res.append(db.contains(i))
        return res

### Floating-point sets

There is a problem with floating-point sets, i.e. `Float64Set` and `Float32Set`: The standard definition of "equal" and hash-function based on the bit representation don't define a meaningful or desired behavior for the hash set:

   * `NAN != NAN` and thus it is not equivalence relation
   * `-0.0 == 0.0` but `hash(-0.0)!=hash(0.0)`, but `x==y => hash(x)==hash(y)` is neccessary for set to work properly.

This problem is resolved through following special case handling:

   * `hash(-0.0):=hash(0.0)`
   * `hash(x):=hash(NAN)` for any not a number `x`.
   * `x is equal y <=> x==y || (x!=x && y!=y)`

A consequence of the above rule, that the equivalence classes of `{0.0, -0.0}` and `e{x | x is not a number}` have more than one element. In the set these classes are represented by the first seen element from the class.

The above holds also for `PyObjectSet` (this behavior is different from `set` which shows a different behavior for nans)

## Testing:

For testing of the local version in an virtual environment run:

    sh test_install.sh 

in the `tests` subfolder.

For testing of the version from github run:

    sh test_install.sh from-github

For keeping the the virtual enviroment after the tests:

    sh test_install.sh local keep

To install and running tests in currently active environment:

    sh test_in_active_env.sh







## Versions:

  * 0.1.0: Int64Set
  * 0.2.0: Int32Set, Float64Set, Float32Set
  * 0.3.0: PyObjectSet, Maps for Int64/32 and also Float64/32, unique-versions

