# cykhash

cython wrapper for khash

## About:

  * Brings functionality of khash (https://github.com/attractivechaos/klib/blob/master/khash.h) to Cython and can be used seamlessly in numpy or pandas.

  * Numpy's world is lacking the concept of a (hash-)set. This shortcoming is fixed and thus efficient `unique` and `isin` implementations are possible.

  * Python-set has a big memory-footprint. For some datatypes the overhead can be reduced by using khash.

  * Is inspired by usage of khash in pandas.
  
  * For python2 and python3.

## Dependencies:

  * Cython + build tool chain (for example gcc on Linux)
  * `virtualenv`+`sh` for testing

## Instalation:

To install the module using pip run:

    pip install https://github.com/realead/cykhash/zipball/master

It is possible to uninstall it afterwards via

    pip uninstall cykhash

You can also install using the `setup.py` file from the root directory of the project:

    python setup.py install

However, there is no easy way to deinstall it afterwards (only manually) if `setup.py` was used directly.


## Usage:

#### A: Int64Set

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

