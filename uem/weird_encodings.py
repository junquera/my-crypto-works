import base64
import sys

# From https://gist.github.com/tunelko/49b7e64c1688d62d0ecd

atom128 = "/128GhIoPQROSTeUbADfgHijKLM+n0pFWXY456xyzB7=39VaqrstJklmNuZvwcdEC"
megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"
zong22 = "ZKj9n+yf0wDVX1s/5YbdxSo=ILaUpPBCHg8uvNO4klm6iJGhQ7eFrWczAMEq3RTt2"
hazz15 = "HNO4klm6ij9n+J2hyf0gzA8uvwDEq3X1Q7ZKeFrWcVTts/MRGYbdxSo=ILaUpPBC5"
b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

class B64weird_encodings:

    def __init__(self, translation):
        b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        self.srch = dict(zip(b, translation))
        self.revlsrch = dict(zip(translation, b))

    def encode(self, pt):
        global srch
        b64 = base64.b64encode(pt)
        r = "".join([self.srch[x] for x in b64])
        return r

    def decode(self, code):
        global revlsrch
        b64 = "".join([self.revlsrch[x] for x in code])
        r = base64.b64decode(b64)
        return r

def encode(variant, pt):
    encoder = B64weird_encodings(variant)
    return encoder.encode(pt)

def decode(variant, code):
    try:
        encoder = B64weird_encodings(variant)
        return encoder.decode(code)
    except KeyError:
        return "Not valid"
    except TypeError:
        return "Padding iccorrect"



with open('base64.txt') as f:
    pt = f.read().replace('\n', '')
    with open('base64.txt', 'wb+') as f:
        f.write(decode(b64, pt))
    with open('atom128.txt', 'wb+') as f:
        f.write(decode(atom128, pt))
    with open('megan35.txt', 'wb+') as f:
        f.write(decode(megan35, pt))
    with open('hazz15.txt', 'wb+') as f:
        f.write( decode(hazz15, pt))
    with open('zong22.txt', 'wb+') as f:
        f.write(decode(zong22, pt))
