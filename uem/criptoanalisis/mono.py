#!/bin/env python3

'''
[     ANÁLISIS ESTADÍSTICO DE TEXTO      ]
[ CIFRADO POR SUSTITUCIÓN MONOALFABÉTICA ]

Javier Junquera Sánchez <javier@junquera.xyz>

Fases:
1. Análisis de entropía
2. Análisis de aparición de caracteres
3. Análisis de caracteres repetidos juntos (RR, LL)
4. Análisis de dupletas repetidas
5. Generación de posibles traducciones basado en estadísticas de idioma
6. Uso de estadísticas para cifrado afín
7. Fuerza bruta afín, césar y atbash
'''
import re
from affine import decode_affine, affine_break

# BASADO EN EL QUIJOTE
estadisticas_castellano = {'A': 0.1203914356874436, 'B': 0.015130070791165134, 'C': 0.03719184102245509, 'D': 0.05437026585244542, 'E': 0.1386395633977034, 'F': 0.004934755557097172, 'G': 0.01092558720618012, 'H': 0.012658047516610746, 'I': 0.048772133465719646, 'J': 0.006582358140488471, 'K': 8.238012916956494e-05, 'L': 0.05551801306561237, 'M': 0.02788784162203377, 'N': 0.06781866708951004, 'O': 0.09582667220822723, 'P': 0.022245112473652295, 'Q': 0.02013110209127842, 'R': 0.06325617061234451, 'S': 0.07834783863652835, 'T': 0.03919621769909202, 'U': 0.048757887277968516, 'V': 0.011134324826707514, 'W': 0.00016847665514377192, 'X': 0.00025209558324821755, 'Y': 0.015759380650084517, 'Z': 0.004021760742090114}

estadisticas_castellano_esp = {' ': 1, 'A': 0.1203914356874436, 'B': 0.015130070791165134, 'C': 0.03719184102245509, 'D': 0.05437026585244542, 'E': 0.1386395633977034, 'F': 0.004934755557097172, 'G': 0.01092558720618012, 'H': 0.012658047516610746, 'I': 0.048772133465719646, 'J': 0.006582358140488471, 'K': 8.238012916956494e-05, 'L': 0.05551801306561237, 'M': 0.02788784162203377, 'N': 0.06781866708951004, 'O': 0.09582667220822723, 'P': 0.022245112473652295, 'Q': 0.02013110209127842, 'R': 0.06325617061234451, 'S': 0.07834783863652835, 'T': 0.03919621769909202, 'U': 0.048757887277968516, 'V': 0.011134324826707514, 'W': 0.00016847665514377192, 'X': 0.00025209558324821755, 'Y': 0.015759380650084517, 'Z': 0.004021760742090114}
# estadisticas_castellano = estadisticas_castellano_esp

# BASADO EN EL SEÑOR DE LOS ANILLO
estadisticas_ingles = {'A': 0.0831295411584481, 'B': 0.01738984496652256, 'C': 0.017155136950865266, 'D': 0.052443360917834525, 'E': 0.12285071813081565, 'F': 0.024581248091420035, 'G': 0.02449291711778557, 'H': 0.06476679361089449, 'I': 0.06393143497452282, 'J': 0.0006511254627912083, 'K': 0.009077900347519288, 'L': 0.04530117076396197, 'M': 0.022928197013403595, 'N': 0.06837322107728455, 'O': 0.0779066568745473, 'P': 0.013705181494913397, 'Q': 0.00058677003914324, 'R': 0.05933696247447866, 'S': 0.05987073392944122, 'T': 0.08989443186779629, 'U': 0.02559074493295679, 'V': 0.008983260018625218, 'W': 0.026715072040218356, 'X': 0.000682672239089232, 'Y': 0.019290222770715505, 'Z': 0.00036468073400515346}

with open('t.txt') as f:
  t = f.read().replace(' ', '').replace('\n', '')

KEYWORDS = ['CRIP', 'CUANDO', 'EN', 'HA', 'HABIA', 'ERA', 'CONTRA', 'DESDE', 'SOLO', 'PERO', 'LE', 'SI', 'ESTA', 'AHORA', 'ALLI', 'SE', 'SEGUN', 'ANTE', 'SER', 'EL', 'POR', 'PARA', 'TAMBIEN', 'TODO', 'SUS', 'PORQUE', 'AQUI', 'YA', 'HACIA', 'A', 'CON', 'HAN', 'DEL', 'Y', 'AL', 'COMO', 'HASTA', 'QUE', 'O', 'UN', 'BAJO', 'LO', 'MAS', 'SU', 'LOS', 'SIN', 'NO', 'PUEDE', 'DOS', 'ENTRE', 'SOBRE', 'CIFR', 'MI', 'FUE', 'MUY', 'TRAS', 'LAS', 'LA', 'ES', 'SON', 'VEZ', 'ME', 'CABE', 'YO', 'HAY', 'ESTE', 'UNA', 'AÑOS', 'DE']
KEYWORDS_EN = list(set(['THE', 'IS', 'AND', 'WHO', 'HE', 'IT', 'WHERE', 'CRYPT', 'A']))

class Descifrado():

    def __init__(self, text, key):
        self.text = text
        self.key = key

    def __str__(self):
        return "[%s] %s" % (self.key, self.text)

MAX = 5
def analiza_repetidos(t,i=2):
    t = re.sub(r'[^A-Z]', '', t.upper())

    res = {}
    for j in range(len(t)):
        ocur = t[j:j+i]

        if len(ocur) < i:
            continue

        last = t[j:].find(ocur)
        while last >= 0:
            if ocur in res:
                res[ocur].append(j+last)
            else:
                res[ocur] = [j+last]

            n = t[j+last+1:].find(ocur)
            if n >= 0:
                last += n + 1
            else:
                last = -1

    for x in res:
        val = list(set(res[x]))
        val.sort()
        res[x] = val

    return res

def calcula_distancias(v):
    dist = []
    for x in range(len(v))[1:]:
        dist.append(v[x] - v[x-1])
    return dist

def divisores(x):
    res = []
    for i in range(int(x/2))[2:]:
        if x % i == 0:
            res.append(i)

    return res

def analisis_estadistico(txt):
    txt = re.sub(r'[^A-Z]', '', txt.upper())
    d = {chr(c + ord('A')): 0 for c in range(ord('Z') - ord('A') + 1)}
    for x in txt:
        if x in d:
            d[x] += 1
        else:
            d[x] = 1
    return {x: float(d[x])/len(txt) for x in d}

def gen_keys(cs, n, key):

    if len(key) == len(cs):
        return [key]

    keys = []
    for c in cs[n]:
        keys += gen_keys(cs, n+1, key + c)

    return keys

from math import gcd
def comun_divisor(values):

    res = values[0]
    for v in values[1:]:
        aux = gcd(res, v)
        if aux <= 2:
            return res
        res = aux

    return res

def repetidos(t):
    res = {}
    for x in range(len(t) - 1):
        if t[x] == t[x+1]:
            c = t[x:x+1]

            if c in res:
                res[c].append(x)
            else:
                res[c] = [x]
    return res

def representa_matrix(t, n=10):
    res = ""
    for i in range(len(t)):
        if i % n == 0 and i > 0:
            res += "\n"
        res += "%c " % t[i]

    return res



def translate(t, translations, n=1):
    res = ""
    while len(t):
        c = t[:n]
        t = t[n:]
        res += translations.get(c, " ")

    return res


def gen_translations(translations, translation):

    translation_aux = {k: translation[k] for k in translation}

    if len(translations) == 0:
        r = translate(t, translation, n=n_gram)
        trans_res.append(Descifrado(r, translation))

        return

    ts = translations.keys()
    for i in ts:
        ts_values = translations[i]
        for j in ts_values:
            # print(it)
            # input(ts_values)
            # input(j)
            translation_aux[i] = j
            # input(translations)
            next = {k: translations[k] for k in translations if k!=i}
            # input(next)
            gen_translations(next, translation_aux)

        break
english = False

def most_able(candidates, KEYWORDS=[]):

    res = {}
    for c in candidates:
        kws = 0
        for keyword in KEYWORDS:
            if keyword in c.text:
                kws += 1

        if english:
            for keyword in KEYWORDS_EN:
                if keyword in c.text:
                    kws += 1

        res[c] = kws

    return {x[0]: x[1] for x in sorted(res.items(), key=lambda x: (x[1],x[0].text))[::-1]}

from entro import entropy


# Entropía del texto
e = entropy(t)

# Análisis estadístico de los caracteres del texto

multigram = False
if multigram:
    print("ANÁLISIS POLIALFABÉTICO")
    n_gram = int(input("Ngram > "))
else:
    print("- ANÁLISIS MONOALFABÉTICO:")
    n_gram = 1

ar = analiza_repetidos(t, i=n_gram)
d = {x: len(ar[x]) for x in ar}

estadisticas = {x[0]: x[1] for x in sorted(d.items(), key=lambda x: (x[1],x[0]))[::-1]}
conv_estadisticas_es = {x[0]: x[1] for x in sorted(estadisticas_castellano.items(), key=lambda x: (x[1],x[0]))[::-1]}
conv_estadisticas_en = {x[0]: x[1] for x in sorted(estadisticas_ingles.items(), key=lambda x: (x[1],x[0]))[::-1]}

r_std = [v  for i, v in enumerate(estadisticas)]
r_mix_es = [v  for i, v in enumerate(conv_estadisticas_es)]
r_mix_en = [v  for i, v in enumerate(conv_estadisticas_en)]


# Tabla de posibles traducciones
translations = {r_std[i]: [r_mix_es[i]] for i in range(min(len(r_std), len(r_mix_es)))}

if english:
    for i in range(min(len(r_std), len(r_mix_en))):
        c = r_mix_en[i]
        tr = r_std[i]
        if c in translations:
            translations[tr].append(c)
        else:
            translations[tr] = [c]



# Caracteres iguales juntos pueden ser LL, RR
rep = repetidos(t)
add_rep = True and (n_gram == 1)
if add_rep:
    for d in rep:
        translations[d].append('L')
        translations[d].append('R')

# Caracteres diferentes repetidos juntos pueden ser CH
dup = analiza_repetidos(t, i=2)
add_dup = False and (n_gram == 1)
if add_dup:
    for r in dup:
        translations[r[0]].append('C')
        translations[r[1]].append('H')

# Representación matriz
mat = representa_matrix(t, n = 20)

def unifica(translations):
    for x in translations:
        translations[x] = list(set(translations[x]))
    return translations

translations = unifica(translations)

print()
print("[*] Mensaje:")
print(t)
print()
print("[*] Entropía: %f" % e)
print()
print("[*] Estadísticas:")
print(estadisticas)
print()
print("[*] Repetidos (RR, LL):")
print(rep)
print()
print("[*] Parejas repetidas:")
print(dup)
print()
print("[*] Matriz:")
print(mat)
print()
print("[*] Traducciones")
print(translations)

claves = 1
for i in translations:
    v = translations[i]
    claves *= len(v) if len(v) > 0 else 1


print()
print("[*] Claves posibles: %d" % claves)

# Resultados de la traducción
trans_res = []
gen_translations(translations, {})

'''
AFFINE ANALYSIS

    C = ord('C') - ord('A')
    D = ord('D') - ord('A')
    L = ord('L') - ord('A')
    A = ord('A') - ord('A')

    # (a * L) + b  = C
    # (a * A) + b  = D

    # b = D - (a * A)
    # (a * L) + D - (a * A) = C
    # a * (L - A) = C - D
    # a = (C - D) * (L - A)**(-1)

    a = ( inverso(L - A, l) * (C - D) ) % l
    # a = 7
    b = ( D - (a * A) )
    # b = 3
'''
stat = most_able(trans_res, KEYWORDS=KEYWORDS)

affine_values = dict(a=[], b=[])
print()
print('-[CODEBOOK BY CRYPTOANALYSIS]')
n_best = 3
for k in stat:
    if n_best:
        m = k.text
        print("[%d] %s" % (stat[k], k))
        broken = affine_break(m[0], m[1], t[0], t[1])
        affine_values['a'].append(broken['a'])
        affine_values['b'].append(broken['b'])
    else:
        break
    n_best -= 1

affine_values['a'] = list(set(affine_values['a']))
affine_values['b'] = list(set(affine_values['b']))

affines = []
for a in affine_values['a']:
    for b in affine_values['b']:
        aux = decode_affine(t, a, b)
        affines.append(Descifrado(aux, broken))
print()
print('-[AFFINE BY CRYPTOANALYSIS]')
n_best = 3
for x in most_able(affines, KEYWORDS=KEYWORDS):
    if n_best:
        print("%s" % x)
    else:
        break
    n_best -= 1

others = True
if others:
    '''
    AFFINE ANALYSIS MANUAL

        C = ord('C') - ord('A')
        D = ord('D') - ord('A')
        L = ord('L') - ord('A')
        A = ord('A') - ord('A')
        # (a * L) + b  = C
        # (a * A) + b  = D

        # b = D - (a * A)
        # (a * L) + D - (a * A) = C
        # a * (L - A) = C - D
        # a = (C - D) * (L - A)**(-1)

        a = ( inverso(L - A, l) * (C - D) ) % l
        # a = 7
        b = ( D - (a * A) )
        # b = 3
    '''
    print()
    print("-[AFFINE BRUTEFORCE]")
    affines = []
    for i in range(26):
        for j in range(26):
            aux = decode_affine(t, i, j)
            # input("%d %d %s" % (i, j, aux))
            affines.append(Descifrado(aux, dict(a=i, b=j)))

    n_best = 3
    for x in most_able(affines, KEYWORDS=KEYWORDS):
        if n_best:
            print("%s" % x)
        else:
            break
        n_best -= 1

    # CESAR ANALYSIS
    from cesar import cesar

    print()
    print("-[CESAR BRUTEFORCE]")
    cesars = []
    for i in range(25):
        cesars.append(Descifrado(cesar(i, t), dict(rot=i)))

    stat = most_able(cesars, KEYWORDS=KEYWORDS)

    n_best = 3
    for k in stat:
        if n_best:
            print("%s" % (k))
        else:
            break
        n_best -= 1

        print()
    print("-[ATBASH]")
    letras = [chr(x + ord('A')) for x in range(ord('Z') - ord('A') + 1)]
    atbash_code = letras[::-1]

    def atbash(t):
        res = ""
        for x in t:
            res += atbash_code[letras.index(x)]
        return res

    print("%s" % atbash(t))
