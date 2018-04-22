import math

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

from Crypto.PublicKey import RSA

k = RSA.generate(1024)

print("Square area calc!")
s1 = int(input("A side: "))
s2 = int(input("Other side: "))

sp1 = pow(s1, k.e, k.n)
sp2 = pow(s2, k.e, k.n)
rp = int(sp1 *  modinv(sp2, k.n))

print("%d / %d = %d" % (sp1, sp2, rp))

print("The area: %d" % pow(rp, k.d, k.n))
