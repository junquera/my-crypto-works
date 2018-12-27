#!/usr/bin/env python
import sys

from math import log

def entropy(b):
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
    return result

if __name__ == '__main__':

    with open(sys.argv[1]) as f:
        b = f.read()

    result = entropy(b)
    print(result)
# Porcentaje
# print(result/8)
