import math

(e, N) = (0x3, 0x64ac4671cb4401e906cd273a2ecbc679f55b879f0ecb25eefcb377ac724ee3b1)
d = 0x431d844bdcd801460488c4d17487d9a5ccc95698301d6ab2e218e4b575d52ea3
c = 0x599f55a1b0520a19233c169b8c339f10695f9e61c92bd8fd3c17c8bba0d5677e

def binaryPows(n):
    x = n
    pows = []
    while x > 0:
        n = int(math.log(x, 2))
        pows.append(n)
        x -= 2**n
    return pows

def modularPow(c, pow, N):
    MAX_BIN_POW=10
    if pow <= 2**MAX_BIN_POW:
        return (c ** pow) % N

    pows = binaryPows(pow)
    results = []
    for p in pows:
        if(p > MAX_BIN_POW):
            results.append((modularPow(c, 2**(p-1), N)**2) % N)
        else:
            results.append(modularPow(c, 2**p, N))

    result = results.pop() % N
    while len(results) > 0:
        result = (result * results.pop()) % N


    return result

print("%x"%modularPow(c,d,N))
