import pytest

import numpy as np

from cykhash import isin_int64, Int64Set_from, Int64Set_from_buffer
from cykhash import isin_int32, Int32Set_from, Int32Set_from_buffer
from cykhash import isin_float64, Float64Set_from, Float64Set_from_buffer
from cykhash import isin_float32, Float32Set_from, Float32Set_from_buffer
from cykhash import isin_pyobject,  PyObjectSet_from, PyObjectSet_from_buffer

ISIN={'int32': isin_int32, 'int64': isin_int64, 'float64' : isin_float64, 'float32' : isin_float32, 'pyobject' : isin_pyobject}
NPTYPE = {'int32': np.int32, 'int64': np.int64, 'float64' : np.float64, 'float32' : np.float32, 'pyobject' : np.object_}
FROM_BUFFER_SET={'int32': Int32Set_from_buffer, 'int64': Int64Set_from_buffer, 'float64' : Float64Set_from_buffer, 'float32' : Float32Set_from_buffer, 'pyobject' : PyObjectSet_from_buffer}



@pytest.mark.parametrize(
    "value_type",
    ['int64', 'int32', 'float64', 'float32', 'pyobject']
)
def test_isin_random(value_type):
        np.random.seed(42)
        NMAX = 10000
        for _ in range(50):
            n = np.random.randint(500, 2000,1)[0]
            values = np.random.randint(0, NMAX, n).astype(NPTYPE[value_type])
            s=FROM_BUFFER_SET[value_type](values, .1)       
            query = np.arange(NMAX).astype(NPTYPE[value_type])
            expected = np.in1d(query, values)
            result = np.empty_like(expected)
            ISIN[value_type](query, s, result)
            assert np.array_equal(expected, result)

