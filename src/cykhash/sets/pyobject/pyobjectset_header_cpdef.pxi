#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t header
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t
#
#

cpdef PyObjectSet PyObjectSet_from_buffer(object[:] buf, double size_hint=*)


from libc.stdint cimport  uint8_t
cpdef void isin_pyobject(object[:] query, PyObjectSet db, uint8_t[:] result) except *

cpdef bint all_pyobject(object[:] query, PyObjectSet db) except *
cpdef bint all_pyobject_from_iter(object query, PyObjectSet db) except *

cpdef bint none_pyobject(object[:] query, PyObjectSet db) except *
cpdef bint none_pyobject_from_iter(object query, PyObjectSet db) except *

cpdef bint any_pyobject(object[:] query, PyObjectSet db) except *
cpdef bint any_pyobject_from_iter(object query, PyObjectSet db) except *

cpdef size_t count_if_pyobject(object[:] query, PyObjectSet db) except *
cpdef size_t count_if_pyobject_from_iter(object query, PyObjectSet db) except *

cpdef void swap_pyobject(PyObjectSet a, PyObjectSet b) except *

# for drop-in replacements:
cpdef bint aredisjoint_pyobject(PyObjectSet a, PyObjectSet b) except *
cpdef bint issubset_pyobject(PyObjectSet s, PyObjectSet sub) except *
cpdef PyObjectSet copy_pyobject(PyObjectSet s)
cpdef void update_pyobject(PyObjectSet s, PyObjectSet other) except *
cpdef PyObjectSet intersect_pyobject(PyObjectSet a, PyObjectSet b)
cpdef PyObjectSet difference_pyobject(PyObjectSet a, PyObjectSet b)

