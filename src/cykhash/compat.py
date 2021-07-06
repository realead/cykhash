import sys
import platform



PYPY = platform.python_implementation() == "PyPy"

def assert_if_not_on_PYPY(statement, reason):
    assert PYPY or statement



IS64BIT = sys.maxsize > 2 ** 32

def assert_equal_32_or_64(val, expected32, expected64, reason):
    if IS64BIT:
        assert val == expected64
    else:
        assert val == expected32
