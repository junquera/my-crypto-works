'''
Public-Key: (512 bit)
Modulus:
    00:ac:e5:e5:58:20:49:76:ff:26:6d:a8:aa:43:de:
    45:0c:2d:a6:61:a5:2e:72:53:36:b7:b8:2c:ac:77:
    55:49:63:b4:bc:d8:5a:3e:31:a0:6f:9a:1c:1a:2e:
    c0:94:fb:0f:27:a2:6e:96:ac:08:7f:18:75:ea:eb:
    e3:32:06:4c:d5
Exponent: 65537 (0x10001)
Public-Key: (520 bit)
Modulus:
    00:fb:2b:a7:0c:79:e8:e4:e5:2a:d1:80:5a:7d:b8:
    6e:8e:47:52:0d:f1:62:d9:f3:9d:38:f5:5f:ff:07:
    ab:ba:4b:60:d2:15:13:9e:d8:c6:8c:ab:df:34:ce:
    38:12:6e:7e:04:cd:cd:d2:92:d1:17:39:4e:2e:33:
    65:49:02:91:0b:e9
Exponent: 65537 (0x10001)

Message: 0xf5ed9da29d8d260f22657e091f34eb930bc42f26f1e023f863ba13bee39071d1ea988ca62b9ad59d4f234fa7d682e22ce3194bbe5b801df3bd976db06b944da
'''
import math
from Crypto.PublicKey import RSA
from math import sqrt

def is_prime(a):
    if a < 2: return False
    for x in range(2, int(sqrt(a)) + 1):
        if a % x == 0:
            return False
    return True

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

def modinv(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1

    if math.gcd(a, m) != 1:
        raise Exception("No mod inverse if a & m aren't relatively prime")

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

pub1 = RSA.importKey(open('pub1').read())
pub2 = RSA.importKey(open('pub2').read())

e = pub1.e

N1 = pub1.n
N2 = pub2.n

p = math.gcd(N1, N2)

q1 = N1//p
q2 = N2//p

c = 0xf5ed9da29d8d260f22657e091f34eb930bc42f26f1e023f863ba13bee39071d1ea988ca62b9ad59d4f234fa7d682e22ce3194bbe5b801df3bd976db06b944da


phi1 = (p-1)*(q1-1)
phi2 = (p-1)*(q2-1)


d1 = modinv(e, phi1)
d2 = modinv(e, phi2)

m = modularPow(c, d1, N1)

print("%x" % m)
