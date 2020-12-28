import subprocess
import os

import cykhash

dir_name = os.path.dirname(cykhash.__file__)

print("Cykhash installation/doctests search path is:", dir_name) 

args = ["--doctest-glob=*.pyx",
        "--doctest-glob=*.pxi",
        "-vv",
        "--doctest-continue-on-failure",
]
command=["pytest"]+args+[dir_name]


subprocess.run(command)  
