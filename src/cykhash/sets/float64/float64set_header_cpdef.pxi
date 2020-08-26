#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t header
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t
#
#

cpdef Float64Set Float64Set_from_buffer(float64_t[:] buf, double size_hint=*)


from libc.stdint cimport  uint8_t
cpdef void isin_float64(float64_t[:] query, Float64Set db, uint8_t[:] result) except *

cpdef bint all_float64(float64_t[:] query, Float64Set db) except *
cpdef bint all_float64_from_iter(object query, Float64Set db) except *

cpdef bint none_float64(float64_t[:] query, Float64Set db) except *
cpdef bint none_float64_from_iter(object query, Float64Set db) except *

cpdef bint any_float64(float64_t[:] query, Float64Set db) except *
cpdef bint any_float64_from_iter(object query, Float64Set db) except *

cpdef size_t count_if_float64(float64_t[:] query, Float64Set db) except *
cpdef size_t count_if_float64_from_iter(object query, Float64Set db) except *

# for drop-in replacements:
cpdef bint aredisjoint_float64(Float64Set a, Float64Set b) except *
cpdef bint issubset_float64(Float64Set s, Float64Set sub) except *

