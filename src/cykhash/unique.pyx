from cpython cimport buffer


from .khashsets cimport khint_t, element_n_from_size_hint
from .khashsets cimport Int64Set, Int64Set_from_buffer, kh_exist_int64set
from .khashsets cimport Int32Set, Int32Set_from_buffer, kh_exist_int32set
from .khashsets cimport Float64Set, Float64Set_from_buffer, kh_exist_float64set
from .khashsets cimport Float32Set, Float32Set_from_buffer, kh_exist_float32set


include "common.pxi"
include "memory.pxi"

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
        cykhash_traced_free(self.ptr)
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


include "unique/unique_impl.pxi"
