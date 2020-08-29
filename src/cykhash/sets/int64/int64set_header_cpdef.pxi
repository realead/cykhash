#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t header
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t
#
#

cpdef Int64Set Int64Set_from_buffer(int64_t[:] buf, double size_hint=*)


from libc.stdint cimport  uint8_t
cpdef void isin_int64(int64_t[:] query, Int64Set db, uint8_t[:] result) except *

cpdef bint all_int64(int64_t[:] query, Int64Set db) except *
cpdef bint all_int64_from_iter(object query, Int64Set db) except *

cpdef bint none_int64(int64_t[:] query, Int64Set db) except *
cpdef bint none_int64_from_iter(object query, Int64Set db) except *

cpdef bint any_int64(int64_t[:] query, Int64Set db) except *
cpdef bint any_int64_from_iter(object query, Int64Set db) except *

cpdef size_t count_if_int64(int64_t[:] query, Int64Set db) except *
cpdef size_t count_if_int64_from_iter(object query, Int64Set db) except *

# for drop-in replacements:
cpdef bint aredisjoint_int64(Int64Set a, Int64Set b) except *
cpdef bint issubset_int64(Int64Set s, Int64Set sub) except *
cpdef Int64Set copy_int64(Int64Set s)
cpdef void update_int64(Int64Set s, Int64Set other) except *

