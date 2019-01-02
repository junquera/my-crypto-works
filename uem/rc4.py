class RC4():

    @staticmethod
    def ksa(key, n):

        S = [i for i in range(n)]

        j = 0

        for i in range(len(S)):
            j = (j + S[i] + key[i % len(key)]) % len(S)
            aux = S[i]
            S[i] = S[j]
            S[j] = aux

        return S

    def __init__(self, k, n=256):
        self.S = RC4.ksa(k, n)
        self.i = 0
        self.j = 0

    def cipher(self, m):
        for c in m:
            self.i = (self.i + 1) % len(self.S)
            self.j = (self.j + self.S[self.i]) % len(self.S)

            aux = self.S[self.i]
            self.S[self.i] = self.S[self.j]
            self.S[self.j] = aux

            k = self.S[(self.S[self.i] + self.S[self.j]) % len(self.S)]

            yield c ^ k


# https://en.wikipedia.org/wiki/RC4
# https://www.geeksforgeeks.org/computer-network-rc4-encryption-algorithm/
if __name__ == '__main__':

    key =  [1, 7, 1, 7]
    message = [0, 1, 2, 3]

    res = []
    for c in RC4(key, 4).cipher(message):
        res.append(c)

    print(res)
