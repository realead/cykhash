#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t header
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t
#
#

cpdef Int32Set Int32Set_from_buffer(int32_t[:] buf, double size_hint=*)


from libc.stdint cimport  uint8_t
cpdef void isin_int32(int32_t[:] query, Int32Set db, uint8_t[:] result) except *

cpdef bint all_int32(int32_t[:] query, Int32Set db) except *
cpdef bint all_int32_from_iter(object query, Int32Set db) except *

cpdef bint none_int32(int32_t[:] query, Int32Set db) except *
cpdef bint none_int32_from_iter(object query, Int32Set db) except *

cpdef bint any_int32(int32_t[:] query, Int32Set db) except *
cpdef bint any_int32_from_iter(object query, Int32Set db) except *

cpdef size_t count_if_int32(int32_t[:] query, Int32Set db) except *
cpdef size_t count_if_int32_from_iter(object query, Int32Set db) except *

cpdef void swap_int32(Int32Set a, Int32Set b) except *

# for drop-in replacements:
cpdef bint aredisjoint_int32(Int32Set a, Int32Set b) except *
cpdef bint issubset_int32(Int32Set s, Int32Set sub) except *
cpdef Int32Set copy_int32(Int32Set s)
cpdef void update_int32(Int32Set s, Int32Set other) except *
cpdef Int32Set intersect_int32(Int32Set a, Int32Set b)

