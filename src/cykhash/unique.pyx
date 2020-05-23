from cpython cimport buffer
from libc.stdlib cimport malloc, realloc, free


from .khashsets cimport khint_t, element_n_from_size_hint
from .khashsets cimport Int64Set, Int64Set_from_buffer, kh_exist_int64set
from .khashsets cimport Int32Set, Int32Set_from_buffer, kh_exist_int32set
from .khashsets cimport Float64Set, Float64Set_from_buffer, kh_exist_float64set
from .khashsets cimport Float32Set, Float32Set_from_buffer, kh_exist_float32set



cdef char *empty_buf=""

# responsible for freeing the data (so we are sure "right" free is called) and 
# can expose the data via buffer interface
# 
cdef class MemoryNanny:

    cdef void*       ptr
    cdef Py_ssize_t  n
    cdef Py_ssize_t  element_size
    cdef Py_ssize_t  buffer_lock_cnt
    cdef bytes       format

    def __cinit__(self):
        self.ptr = NULL
        self.n = 0
        self.element_size = 0
        self.buffer_lock_cnt = 0
        self.format = None 

    def __dealloc__(self):      
        free(self.ptr)
        self.ptr=NULL 

    def __getbuffer__(self, buffer.Py_buffer *view, int flags):
        #is input sane?
        if(view==NULL):
            raise BufferError("view==NULL argument is obsolete")


        #should never happen, just to be sure
        if NULL == self.ptr:
            view.buf = empty_buf
        else:
            view.buf = self.ptr

        view.obj = self; # increments ref count
       
        
        # size of the memory-block in bytes
        view.len = self.n * self.element_size

         
        # 0 or 1 possible as long as the same for all
        view.readonly = 0

        # should be original value, even if buffer.format is set to NULL
        view.itemsize = self.element_size;

        # format:
        if (flags & buffer.PyBUF_FORMAT) == buffer.PyBUF_FORMAT:
             view.format = self.format
        else:
             # NULL indicates that the buffer's data type has been cast to 'B'.
             # view->itemsize is the _previous_ itemsize. n * itemsize = len still holds at this
             # point. The equality calcsize(format) = itemsize does _not_ hold
             # from here on! */
             view.format = NULL

        # data is one-dimensional
        view.ndim = 1;
        

        view.shape = NULL
        view.strides = NULL
        view.suboffsets = NULL

        # no need for internal data
        view.internal = NULL

        self.buffer_lock_cnt+=1


    def __releasebuffer__(self, buffer.Py_buffer *view):
        self.buffer_lock_cnt-=1


    @staticmethod
    cdef MemoryNanny create_memory_nanny(void* ptr, Py_ssize_t  n, Py_ssize_t element_size, object format):
        cdef MemoryNanny nanny = MemoryNanny()
        nanny.ptr = ptr
        nanny.n   = n
        nanny.element_size = element_size
        nanny.format =  format
        return nanny


# TODO: reduce code duplication

cpdef unique_int64(int64_t[:] vals, double size_hint=0.0):
    cdef Int64Set s = Int64Set_from_buffer(vals, size_hint)
    
    # compress:
    cdef int64_t* mem = s.table.keys
    cdef khint_t i
    cdef khint_t current = 0
    for i in range(s.table.n_buckets):
        if kh_exist_int64set(s.table, i):
            mem[current] = mem[i]
            current += 1

    # take over the memory:
    s.table.keys = NULL
    
    # shrink to fit:
    mem = <int64_t*> realloc(mem, sizeof(int64_t)*current);
    return MemoryNanny.create_memory_nanny(mem, current, sizeof(int64_t), b"q")


cpdef unique_stable_int64(int64_t[:] vals, double size_hint=0.0):
    # prepare 
    cdef Py_ssize_t n = len(vals)
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=Int64Set(number_of_elements_hint=at_least_needed)
    cdef int64_t* mem = <int64_t*> malloc(sizeof(int64_t)*n);
    
    # insert
    cdef khint_t current = 0
    cdef Py_ssize_t i
    cdef int64_t element
    for i in range(n):
        element = vals[i]
        res.add(element)
        if current != len(res):
            mem[current] = element
            current += 1
    
    # shrink to fit:
    mem = <int64_t*> realloc(mem, sizeof(int64_t)*current);
    return MemoryNanny.create_memory_nanny(mem, current, sizeof(int64_t), b"q")


cpdef unique_int32(int32_t[:] vals, double size_hint=0.0):
    cdef Int32Set s = Int32Set_from_buffer(vals, size_hint)
    

    # compress:
    cdef int32_t* mem = s.table.keys
    cdef khint_t i
    cdef khint_t current = 0
    for i in range(s.table.n_buckets):
        if kh_exist_int32set(s.table, i):
            mem[current] = mem[i]
            current += 1

    # take over the memory:
    s.table.keys = NULL
    
    # shrink to fit:
    mem = <int32_t*> realloc(mem, sizeof(int32_t)*current);
    return MemoryNanny.create_memory_nanny(mem, current, sizeof(int32_t), b"i")


cpdef unique_stable_int32(int32_t[:] vals, double size_hint=0.0):
    # prepare 
    cdef Py_ssize_t n = len(vals)
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=Int32Set(number_of_elements_hint=at_least_needed)
    cdef int32_t* mem = <int32_t*> malloc(sizeof(int32_t)*n);
    
    # insert
    cdef khint_t current = 0
    cdef Py_ssize_t i
    cdef int32_t element
    for i in range(n):
        element = vals[i]
        res.add(element)
        if current != len(res):
            mem[current] = element
            current += 1
    
    # shrink to fit:
    mem = <int32_t*> realloc(mem, sizeof(int32_t)*current);
    return MemoryNanny.create_memory_nanny(mem, current, sizeof(int32_t), b"i")



cpdef unique_float64(float64_t[:] vals, double size_hint=0.0):
    cdef Float64Set s = Float64Set_from_buffer(vals, size_hint)
    
    # compress:
    cdef float64_t* mem = s.table.keys
    cdef khint_t i
    cdef khint_t current = 0
    for i in range(s.table.n_buckets):
        if kh_exist_float64set(s.table, i):
            mem[current] = mem[i]
            current += 1

    # take over the memory:
    s.table.keys = NULL
    
    # shrink to fit:
    mem = <float64_t*> realloc(mem, sizeof(float64_t)*current);
    return MemoryNanny.create_memory_nanny(mem, current, sizeof(float64_t), b"d")


cpdef unique_stable_float64(float64_t[:] vals, double size_hint=0.0):
    # prepare 
    cdef Py_ssize_t n = len(vals)
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=Float64Set(number_of_elements_hint=at_least_needed)
    cdef float64_t* mem = <float64_t*> malloc(sizeof(float64_t)*n);
    
    # insert
    cdef khint_t current = 0
    cdef Py_ssize_t i
    cdef float64_t element
    for i in range(n):
        element = vals[i]
        res.add(element)
        if current != len(res):
            mem[current] = element
            current += 1
    
    # shrink to fit:
    mem = <float64_t*> realloc(mem, sizeof(float64_t)*current);
    return MemoryNanny.create_memory_nanny(mem, current, sizeof(float64_t), b"d")


cpdef unique_float32(float32_t[:] vals, double size_hint=0.0):
    cdef Float32Set s = Float32Set_from_buffer(vals, size_hint)
    
    # compress:
    cdef float32_t* mem = s.table.keys
    cdef khint_t i
    cdef khint_t current = 0
    for i in range(s.table.n_buckets):
        if kh_exist_float32set(s.table, i):
            mem[current] = mem[i]
            current += 1

    # take over the memory:
    s.table.keys = NULL
    
    # shrink to fit:
    mem = <float32_t*> realloc(mem, sizeof(float32_t)*current);
    return MemoryNanny.create_memory_nanny(mem, current, sizeof(float32_t), b"f")


cpdef unique_stable_float32(float32_t[:] vals, double size_hint=0.0):
    # prepare 
    cdef Py_ssize_t n = len(vals)
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=Float32Set(number_of_elements_hint=at_least_needed)
    cdef float32_t* mem = <float32_t*> malloc(sizeof(float32_t)*n);
    
    # insert
    cdef khint_t current = 0
    cdef Py_ssize_t i
    cdef float32_t element
    for i in range(n):
        element = vals[i]
        res.add(element)
        if current != len(res):
            mem[current] = element
            current += 1
    
    # shrink to fit:
    mem = <float32_t*> realloc(mem, sizeof(float32_t)*current);
    return MemoryNanny.create_memory_nanny(mem, current, sizeof(float32_t), b"f")

