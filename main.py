import math

good_res = '4d801868d894740b2be29309fcd3edcd51bd2c2a685028b89290f9268c727581'

(e, N) = (0x3, 0x64ac4671cb4401e906cd273a2ecbc679f55b879f0ecb25eefcb377ac724ee3b1)
m = 0x4d801868d894740b2be29309fcd3edcd51bd2c2a685028b89290f9268c727581
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
    pows = binaryPows(pow)

    print(pows)
    # TODO Ver como volver a factorizar 'pows'
    results = []
    for p in pows:
        results.append((c**(2**p)) % N)



    result = results.pop() % N
    while len(results) > 0:
        result = (result * results.pop()) % N


    return result


for i in range(10):
    print(binaryPows(i))
'''
print(modularPow(c,d,N))
print(modularPow(m, e, N))
print(m**e % N)
print((m**e % N) == modularPow(m, e, N))
'''
