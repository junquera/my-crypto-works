t = '''VAQG JYHN QGTR YNOQ AEXM TRZR QQAU QAQQ XQZQ YUSA QEFM QZXM OUGP MP'''
t = '''AFOE DNVJ DHFY REBF DRGE BAYR EBCF RRHD NGNY RJMK DWJG HQGZ FSJV FWNJ FHFU ENCN VNVE ESKN C'''

i = ord('A')
f = ord('Z')
r = (f + 1) - i

l = list("".join(t.split()))

def print_four(s):

    aux = s
    res = ""
    while len(aux):
        res += aux[:4]
        res += " "
        aux = aux[4:]

    return res

def cesar(n, l):

    res = []

    for y in l:
        c = chr(((ord(y) - i - n) % r) + i)
        res.append(c)

    return "".join(res)


def permuta(texts):
    m = len(texts[0])
    for text in texts:
        m = m if m < len(text) else len(text)

    res = ""
    for i in range(m):
        for text in texts:
            res += text[i]

    return res


def char_analysis(t):
    res = {}
    for c in t.replace(' ', ''):
        if c in res:
            res[c] += 1
        else:
            res[c] = 1

    return res

def sel(n, t):
    i = 1
    res = ""
    while i <= len(t):
        res += t[((n*i) % len(t))]
        i += 1

    return res

for y in range(len(l))[1:]:
    print(print_four(sel(y, l)))


# 5 13 18
# F N S
# G O T
for x in [5,13,18]:
    c = cesar(x, l)
    for y in range(len(c)):
        print("[%d %d] %s" % (x, y, print_four(sel(y, c))))
