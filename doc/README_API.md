# cykhash API:


## Isin

  * `isin_int64`, `isin_int32`, `isin_float64`, `isin_float32`
  * the signature is `def isin_int64(int64_t[:] query, Int64Set db, uint8_t[:] result)`. `query` and `result` must have the same size, otherwise an exception is raised.
  * Running time is `O(len(query))`s.

## Unique

  * `unique_int64`, `unique_int32`, `unique_float64`, `unique_float32`
  * returns an object which implements the buffer protocol, so `np.ctypeslib.as_array` (recommended) or `np.frombuffer` (less safe, as memory can get reinterpreted) can be used to create numpy arrays.
  * differently as pandas, the returned uniques aren't in the order of the appearance.
  * the signature is `unique_int64(buffer, size_hint=0.0)` the initial memory-consumption of the hash-set will be `len(buffer)*size_hint` unless `size_hint<=0.0`, in this case it will be ensured, that no rehashing is needed even if all elements are unique in the buffer.
  * `unique_stable_int64`, `unique_stable_int32`, `unique_stable_float64`, `unique_stable_float32` order the elements in order of their appearance.

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

#### Utility functions for sets:

The following functions are available:

   * `XXXXSet_from(it)` - creates a `XXXXSet` from an iterable, with `XXXX` being either `Int64`, `Int32`, `Float64`, `Float32` or `PyObject`.
   * `XXXXSet_from_buffer(buf, size_hint=0.0)` creates a `XXXXSet` from an object which implements buffer interface, with `XXXX` being either `Int64`, `Int32`, `Float64`, `Float32` or `PyObject`. Starting size of hash-set is `int(size_hint*len(buf))` unless `size_hint<=0.0`, in which case it will be ensured that no rehashing is needed.
  * `isin_xxxx(query, db, result)` evaluates `isin` for `query` being a buffer of the right type, `db` - a corresponding `XXXXSet`, and result a buffer for with 8bit-itemsize, `xxxx` being either `int64`, `int32`, `float64`, `float32` or `pyobject`.


### Maps

Following classes are defined: 
         
  * `Int64toInt64Map` for mapping  64 bit integers to 64bit integer/floats
  * `Int32toInt32Map` for mapping 32 bit integers to 32bit integer/floats
  * `Float64toInt64Map`for mapping 64 bit floats to 64bit integer/floats
  * `Float32toInt32Map`for mapping 32 bit floats to 32bit integer/floats
  * `PyObjectMap`for arbitrary Python-objects as key/values

with Python interface:

  * `__len__`: number of elements in the map
  * `__contains__`: whether an element is contained in the map
  * `put_intXX/get_intXX`: setting/retrieving elements with XX=32 or 64 bits integer 
  * `put_floatXX/get_floatXX`: setting/retrieving elements with XX=32 or 64 bits float 
  * `__setitem__/__getitem___`: parameter `for_intXX` in the constructor deceides whether elements are intepreted as int or float (XX =  32 or 64 bits)
  * `discard`: remove an element or do nothing if element is not in the map
  * `__iter__`: returns an iterator through all elements in map

with Cython interface:

  * `contains`: checks whether an element is contained in the map
  * `put_intXX/get_intXX,put_floatXX/get_floatXX` : setting/getting elements in the map
  * `discard` : remove an element or do nothing if element is not in the map
  * `get_iter`: returns an iterator with the following Cython interface:
       * `has_next`:returns true if there are more elements in the iterator
       * `next` :returns next element and moves the iterator

#### Utility functions for maps:

The following functions are available:

   * `TypeXXtoXXMap_from_typeXX_buffer(keys, vals, size_hint=0.0)` - creates a `TypeXXtoXXMyp` from buffers with  `Type` either `Float` or `Int`, `XX` either 32 or 64 and `type` either `float` or `int`. Starting size of hash-map is `int(size_hint*min(len(keys), len(vals)))` unless `size_hint<=0.0`, in which case it will be ensured that no rehashing is needed.
   * `PyObjectMap_from_object_buffer` for keys, values as objects.


