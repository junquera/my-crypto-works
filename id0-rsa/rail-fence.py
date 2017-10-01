orig = 'WEAREDISCOVEREDFLEEATONCE'
ciph = 'WECRL TEERD SOEEF EAOCA IVDEN'

n_rails = 3

def crypt(a, n_rails):
    result = []
    for x in range(n_rails):
        result.append([])
    rail = 0
    inc = True
    for c in a:
        result[rail].append(c)
        if inc:
            if rail >= n_rails - 1:
                inc = False
                rail -= 1
            else:
                rail += 1
        else:
            if rail == 0:
                inc = True
                rail += 1
            else:
                rail -= 1

    count = 0
    res = ''
    for i in range(len(result)):
        for j in range(len(result[i])):
            res += result[i][j]
            count += 1
            if count % 5 == 0:
                res += " "

    return res

# a.....      0
# .a...a      pos + 2*(n_rails - pos)
# ..a.a.      pos + 2*(n_rails - pos)
# ...a..      pos

def decrypt(a, n_rails):

    a = a.replace(' ', '')

    n = len(a)

    elements_per_block = 2 + 2*(n_rails - 2)

    values = [0] * n_rails

    sobran = n % elements_per_block

    if sobran > 0:
        values[0] = 1
        for pos in range(n_rails)[1:-1]:
            if sobran > pos:
                    values[pos] += 1
                    if sobran > (2 * n_rails - pos - 2):
                        values[pos] += 1
        values[-1] = sobran / n_rails

    blocks = (n - sobran) / elements_per_block

    values[0] += blocks
    for v in range(len(values))[1:-1]:
        values[v] += 2 * blocks
    values[-1] += blocks


    result = []

    for i in values:
        result.append([x for x in a[:i]])
        a = a[i:]

    dec = ''
    rail = 0
    inc = True

    for c in range(n):
        if len(result[rail]) <= 0:
            break
        dec += result[rail][0]
        result[rail] = result[rail][1:]
        if inc:
            if rail >= n_rails - 1:
                inc = False
                rail -= 1
            else:
                rail += 1
        else:
            if rail == 0:
                inc = True
                rail += 1
            else:
                rail -= 1

    return dec
#
# def decrypt(a, n_rails):
#     rail_len = len(a) / n_rails
#
#     aux = a
#     res = []
#     while len(aux) > 0:
#         res.append([x for x in aux[:rail_len]])
#         aux = aux[rail_len:]
#     for x in res:
#         print(x)
#


ciphered = 'WAPSD EXTCO EEREF SELIO RSARC LIETE OIHHP VASTF EGBER IPAPN TOEGI AIATH DDHIY EACYE RQAEN OHRTE TEVME BGHMF EIOWS GFHCL XEUUC OMTOT LERES SDEWW ORCCS HEURE ATTEG ALSEB APXET IURWV RTEEH IOTLO SNACN NULCV LCMTH HHCOH TIOTD ASNAL TSANA CASOR LEKAS TATCW INTLO TRYER YLTND RILER AOMAX OITDE ECOIA HAALS TYIOA DAEHI OTSTE IEYES HHSNG EHCAT SOUAC EHSST TCODN FSOTS TIIGN LTTNL DUBST TCMIM EHTAO IUUPF TSTTI PUEAY OAEOA EEALA LWGWM GNHYU IAAHD TORYA OLVMH RHTGY IHNNM UAARL MMHID HYFCP GRAET MTCNT HIIIO RCVCL BOTSA OFRNR YEHTG IFHEA WLYSC EEEEY UVEIM SOEUE TAYHN NITEK AERAW DSIAE QTDIE HET'
# ciphered = 'WECRL TEERD SOEEF EAOCA IVDEN'

# for x in range(20):
#     a=("%d\t%s"%(x, decrypt(crypt("A"*x, 10), 10)))

for n_r in range(20)[2:]:
    # print("%d\t%s"%(n_r, decrypt(crypt("ESTOESUNAPRUEBADEVERDAD", n_r), n_r)))
    print("%d\t%s"%(n_r, decrypt(ciphered, n_r)))
