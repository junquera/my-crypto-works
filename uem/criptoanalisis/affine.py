l = ord('Z') - ord('A') + 1

def inverso(x, m):
    for i in range(m):
        r = (x * i) % m
        if r == 1:
            return i

    return 0

def encode_affine(t, a, b):

    res = ""
    for i in t:
        d = chr(ord('A') + (((a * (ord(i) - ord('A'))) +  b) % l))
        res += d
    return res

def decode_affine(t, a, b):

    a = inverso(a, l)
    res = ""
    for i in t:
        d = chr(ord('A') + ((a * ((ord(i) - ord('A')) - b)) % l))
        res += d

    return res



def affine_break(m1, m2, c1, c2):
    # (a * m1) + b = c1
    # (a * m2) + b = c2
    # b = c2 - (a * m2)
    # (a * m1) + c2 -(a * m2) = c1
    # a * (m1 - m2) = c1 - c2
    # ---
    # a = (c1 - c2) * inv(m1 - m2)
    # b = c2 - (a * m2)
    m1 = ord(m1) - ord('A')
    m2 = ord(m2) - ord('A')
    c1 = ord(c1) - ord('A')
    c2 = ord(c2) - ord('A')

    a = ((c1 - c2) * inverso((m1 - m2), l)) % l
    b = (c2 - (a * m2)) % l
    return dict(a=a, b=b)
