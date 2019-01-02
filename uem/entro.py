import sys

with open(sys.argv[1]) as f:
    b = f.read()

from math import log

l = len(b)

count = {}

for i in b:
    if i in count:
        count[i] += 1
    else:
        count[i] = 1
    


result = 0

for v in count:
    f = float(count[v])/l
    result -= (f * log(f, 2))

print(result)
# Porcentaje
# print(result/8)
