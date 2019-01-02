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

# BASADO EN EL QUIJOTE
estadisticas_castellano = {'A': 0.1203914356874436, 'B': 0.015130070791165134, 'C': 0.03719184102245509, 'D': 0.05437026585244542, 'E': 0.1386395633977034, 'F': 0.004934755557097172, 'G': 0.01092558720618012, 'H': 0.012658047516610746, 'I': 0.048772133465719646, 'J': 0.006582358140488471, 'K': 8.238012916956494e-05, 'L': 0.05551801306561237, 'M': 0.02788784162203377, 'N': 0.06781866708951004, 'O': 0.09582667220822723, 'P': 0.022245112473652295, 'Q': 0.02013110209127842, 'R': 0.06325617061234451, 'S': 0.07834783863652835, 'T': 0.03919621769909202, 'U': 0.048757887277968516, 'V': 0.011134324826707514, 'W': 0.00016847665514377192, 'X': 0.00025209558324821755, 'Y': 0.015759380650084517, 'Z': 0.004021760742090114}

estadisticas_castellano_esp = {' ': 1, 'A': 0.1203914356874436, 'B': 0.015130070791165134, 'C': 0.03719184102245509, 'D': 0.05437026585244542, 'E': 0.1386395633977034, 'F': 0.004934755557097172, 'G': 0.01092558720618012, 'H': 0.012658047516610746, 'I': 0.048772133465719646, 'J': 0.006582358140488471, 'K': 8.238012916956494e-05, 'L': 0.05551801306561237, 'M': 0.02788784162203377, 'N': 0.06781866708951004, 'O': 0.09582667220822723, 'P': 0.022245112473652295, 'Q': 0.02013110209127842, 'R': 0.06325617061234451, 'S': 0.07834783863652835, 'T': 0.03919621769909202, 'U': 0.048757887277968516, 'V': 0.011134324826707514, 'W': 0.00016847665514377192, 'X': 0.00025209558324821755, 'Y': 0.015759380650084517, 'Z': 0.004021760742090114}
# estadisticas_castellano = estadisticas_castellano_esp

# BASADO EN EL SEÑOR DE LOS ANILLO
estadisticas_ingles = {'A': 0.0831295411584481, 'B': 0.01738984496652256, 'C': 0.017155136950865266, 'D': 0.052443360917834525, 'E': 0.12285071813081565, 'F': 0.024581248091420035, 'G': 0.02449291711778557, 'H': 0.06476679361089449, 'I': 0.06393143497452282, 'J': 0.0006511254627912083, 'K': 0.009077900347519288, 'L': 0.04530117076396197, 'M': 0.022928197013403595, 'N': 0.06837322107728455, 'O': 0.0779066568745473, 'P': 0.013705181494913397, 'Q': 0.00058677003914324, 'R': 0.05933696247447866, 'S': 0.05987073392944122, 'T': 0.08989443186779629, 'U': 0.02559074493295679, 'V': 0.008983260018625218, 'W': 0.026715072040218356, 'X': 0.000682672239089232, 'Y': 0.019290222770715505, 'Z': 0.00036468073400515346}

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

def distancia_repeticiones(r):

    x = [d for d in r]
    x.sort()

    distancias = []

    for i in range(len(x))[1:]:
        distancias.append(x[i] - x[i - 1])

    return distancias

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

def most_able(candidates, KEYWORDS=KEYWORDS):

    res = {}
    for c in candidates:
        kws = 0
        for keyword in KEYWORDS:
            if keyword in c.text:
                kws += 1

        for keyword in KEYWORDS_EN:
            if keyword in c.text:
                kws += 1

        res[c] = kws

    return [(x[0], x[1]) for x in sorted(res.items(), key=lambda x: (x[1],x[0].text))[::-1]]


# ar = analiza_repetidos(t, i=n_gram)
# d = {x: len(ar[x]) for x in ar}
#
# estadisticas = {x[0]: x[1] for x in sorted(d.items(), key=lambda x: (x[1],x[0]))[::-1]}
# conv_estadisticas_es = {x[0]: x[1] for x in sorted(estadisticas_castellano.items(), key=lambda x: (x[1],x[0]))[::-1]}
# conv_estadisticas_en = {x[0]: x[1] for x in sorted(estadisticas_ingles.items(), key=lambda x: (x[1],x[0]))[::-1]}
#
# r_std = [v  for i, v in enumerate(estadisticas)]
# r_mix_es = [v  for i, v in enumerate(conv_estadisticas_es)]
# r_mix_en = [v  for i, v in enumerate(conv_estadisticas_en)]
#


def traduce(stat, base_stat=estadisticas_castellano):

    # Ordenacion de las letras según su estadística
    stat1_sort = [x[0] for x in sorted(stat.items(), key=lambda x: (x[1],x[0]))[::-1]]
    esp_sort = [x[0] for x in sorted(base_stat.items(), key=lambda x: (x[1],x[0]))[::-1]]

    l = min(len(stat1_sort), len(esp_sort))

    res = {}
    for x in range(l):
        res[stat1_sort[x]] = esp_sort[x]

    return res


def char_diff(x, y):
    return (ord(x) - ord(y)) % (ord('Z') - ord('A') + 1)

def get_greater(dictionary):
    greater = 0
    greater_char = 'A'

    for s in dictionary:
        if dictionary[s] > greater:
            greater = dictionary[s]
            greater_char = s

    return greater_char

def most_common(arr):
    d = {}
    for a in arr:
        if a in d:
            d[a] += 1
        else:
            d[a] = 1

    return get_greater(d)

# Analiza el desplazamiento en el alfabeto
def calc_desplaz(stat, base_stat=estadisticas_castellano, tries=5):

    greaters = []
    base_greaters = []

    aux_stat = {x: stat[x] for x in stat}
    aux_base_stat = {x: base_stat[x] for x in base_stat}

    for _ in range(tries):

        greater_char = get_greater(aux_stat)
        del aux_stat[greater_char]
        greaters.append(greater_char)

        base_greater_char = get_greater(aux_base_stat)
        del aux_base_stat[base_greater_char]
        base_greaters.append(base_greater_char)


    possibles = []
    for x in greaters:
        for y in base_greaters:
            possibles.append(char_diff(x, y))
            # possibles.append(char_diff(y, x))


    x = most_common(possibles)

    # print([chr(x + ord('A')) for x in possibles])
    return x

def unifica(translations):
    for x in translations:
        translations[x] = list(set(translations[x]))
    return translations


def vigenere_enc(m, k):

    res = ""
    for i in range(len(m)):

        a = ord(m[i]) - ord('A')
        b = ord(k[i%len(k)]) - ord('A')

        c = ((a + b) % (ord('Z') - ord('A') + 1))

        res += chr(c + ord('A'))

    return res

def vigenere_dec(m, k):

    res = ""
    for i in range(len(m)):

        a = ord(m[i]) - ord('A')
        b = ord(k[i%len(k)]) - ord('A')

        c = ((a - b) % (ord('Z') - ord('A') + 1))

        res += chr(c + ord('A'))

    return res
