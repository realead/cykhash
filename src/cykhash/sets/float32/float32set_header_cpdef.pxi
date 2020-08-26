#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t header
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t


cpdef Float32Set Float32Set_from_buffer(float32_t[:] buf, double size_hint=*)


from libc.stdint cimport  uint8_t
cpdef void isin_float32(float32_t[:] query, Float32Set db, uint8_t[:] result) except *

cpdef bint all_float32(float32_t[:] query, Float32Set db) except *
cpdef bint all_float32_from_iter(object query, Float32Set db) except *

cpdef bint none_float32(float32_t[:] query, Float32Set db) except *
cpdef bint none_float32_from_iter(object query, Float32Set db) except *

cpdef bint any_float32(float32_t[:] query, Float32Set db) except *
cpdef bint any_float32_from_iter(object query, Float32Set db) except *

cpdef size_t count_if_float32(float32_t[:] query, Float32Set db) except *
cpdef size_t count_if_float32_from_iter(object query, Float32Set db) except *

cpdef bint aredisjoint_float32(Float32Set a, Float32Set b) except *

