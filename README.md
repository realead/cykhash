# cykhash

cython wrapper for khash

## About:

  * Brings functionality of khash (https://github.com/attractivechaos/klib/blob/master/khash.h) to Cython and can be used seamlessly in numpy or pandas.

  * Numpy's world is lacking the concept of a (hash-)set. This shortcoming is fixed and thus efficient `unique` and `isin` implementations are possible.

  * Python-set has a big memory-footprint. For some datatypes the overhead can be reduced by using khash.

  * Is inspired by usage of khash in pandas.
  
  * For python2 and python3.

This project was inspired by the following stackoverflow question: https://stackoverflow.com/questions/50779617/pandas-pd-series-isin-performance-with-set-versus-array

## Dependencies:

Essential:

  * Cython>=0.28 because verbatim C-code feature is used
  * build tool chain (for example gcc on Linux)

Additional dependencies for testing:

  * `sh`
  * `virtualenv`
  * `uttemplate`>=0.2.0 (https://github.com/realead/uttemplate)

## Instalation:

To install the module using pip run:

    pip install https://github.com/realead/cykhash/zipball/master

It is possible to uninstall it afterwards via

    pip uninstall cykhash

You can also install using the `setup.py` file from the root directory of the project:

    python setup.py install

However, there is no easy way to deinstall it afterwards (only manually) if `setup.py` was used directly.

## Performance

Run `sh run_perf_tests.sh` in tests-folder to reproduce. numpy and pandas must be installed in addtion to be able to run the performance tests

#### Memory consumption:

Peak memory usage for N int64-integers (inclusive python-interpreter):

                      10^3       10^4      10^5       10^6      10^7
    python2-set        6MB        6MB      13MB       62MB      502MB
    python3-set        8MB        9MB      17MB       79MB      588MB
    cykhash (p3)      10MB       10MB      10MB       26MB      147MB

i.e. there is about 4 time less memory needed.

#### isin

Compared to pandas' `isin`, which has a linear running time in number of elements in the lookup. cykhash's `isin` has a `O(1)` in the number of elements in the look-up:

    n	pandas(#look-up=10^n)	cykhash(#look-up=10^n)
    2 	 0.0009466878400417045 	 0.0008094332498149015
    3 	 0.0011027359400759451 	 0.001505808719957713
    4 	 0.001315673690114636 	 0.0005093092197785154
    5 	 0.007601776499941479 	 0.00031931002013152465
    6 	 0.11544147745007649 	 0.000292295379913412
    7 	 0.7747500354002114 	 0.00047073251014808195


## Usage:

### Sets

Following classes are defined: 
         
  * `Int64Set` for 64 bit integers
  * `Int32Set` for 32 bit integers
  * `Float64Set`for 64 bit floats (NB: `nan` are not yet handled in a proper way)
  * `Float32Set`for 32 bit floats (NB: `nan` are not yet handled in a proper way)

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

## Testing:

For testing of the local version run (or `p2` for python2):

    sh test_install.sh p3

in the `tests` subfolder.

For testing of the version from github run:

    sh test_install.sh p3 from-github

For keeping the the virtual enviroment after the tests:

    sh test_install.sh p3 local keep

To testing the current version without installing/building:

    sh run_test_from_source.sh

or to run it after the rebuild (without installing):
   
    sh run_test_from_source.sh rebuild





## Versions:

  * 0.1.0: Int64Set
  * 0.2.0: Int32Set, Float64Set, Float32Set

