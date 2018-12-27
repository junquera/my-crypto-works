#!/usr/bin/env python3
t = '''
VAQG  JYHN  QGTR  YNOQ  AEXM  TRZR  QQAU  QAQQ  XQZQ  YUSA  QEFM  QZXM  OUGP  MP
'''

i = ord('A')
f = ord('Z')
r = (f + 1) - i

l = list("".join(t.split()))

def print_four(n, s):

    aux = s
    res = ""
    while len(aux):
        res += aux[:4]
        res += " "
        aux = aux[4:]
    print("[%02d] %s" % (n, res))

def cesar(n, l):

    res = []

    for y in l:
        c = chr(((ord(y) - i + n) % r) + i)
        res.append(c)
    return "".join(res)

if __name__ == '__main__':
    print
    for x in range(r)[:int(r/2) + 1]:

        pos = cesar(-x, l) # []
        neg = cesar(x, l)


        print_four(x, pos)
        print_four(r-x, neg)
