import sys
from cykhash import Int64Set

N=int(sys.argv[1])

s=Int64Set()
for i in range(N):
    s.add(i)

