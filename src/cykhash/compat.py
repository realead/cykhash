import platform

PYPY = platform.python_implementation() == "PyPy"

def assert_if_not_on_PYPY(statement, reason):
    assert PYPY or statement
