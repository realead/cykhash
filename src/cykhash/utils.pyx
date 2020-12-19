include "memory.pxi"

def get_cykhash_trace_domain():
    """
    yield domain number of the cykhash trace domain (as specified by trace malloc),
    using this trace domain it is possible to trace memory allocations done by cykhash
    """
    return CYKHASH_TRACE_DOMAIN

