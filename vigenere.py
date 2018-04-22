msg = '''qv ah pfsix xi wm ughgsm, lk wyja vugfcq vu kytqzu ugzdlglqp, zw nu qfopu nmpyxu kyp hqbíu yy tqjupra lk fsd pm rurkm mt uweutryvz, mlglkl mvzckfm, zuwír qxiii c rmtmi gzdzkxsc. gvg ipwm lk upra uáy penm yay gldvkls, dmtvcgóy xiy gáw yaknyw, ogmriw j cckvvlzbum pze aáhuhze, tkhxpviy fsd hqklrpe, iraúr amtugmya lk uñeoulale waa jiqtzoum, gzzaagíey xiy nvpe xglxpe lk my smkoyrom. tg wsyfzgmiñl bixu wfbmxuv px zkns pe zuwmymvzy. iw dmyns oqtru gzzkroíey eiei hp hmruveq, kgfdle lk piwxcji tldi ruw qumyned owt myd bitnyqxwy xi wa uomqz, xwy xíed pm khxcq akgeym ak bsydihu gzz aa piwxwxc hp xw sám jtzw. zyríl qv yo glei ahe lyi woi amagve oq tum gfmzkhxl, k ctu wznzohe bgm ti pwqogve l xwy pitzbk, s yy ywfi hp oisjs j btgte, bgm gmí iyeqrfemm mr lsníz kugs eaugve wm xuxeoqzg. zvteihu pl qlgx hp zckmxca poxewsw iir waa icrngmtne lñaa, kle oq kugtwqfoóh vpoqg, mina lk weczmy, yrugbu xi caazls; rdit geodcmuhzd g ggmra lk fe nmhg. kytqzkh hpoqx kyp fmtíu iw ewhliyauhli oq yacnlpi u kypeiju (ufq mt ywea pgs ewsctu htrmxyrnui kh pze ianscqa woi oqazy glew kmgcujkh), efzyay tzd kuhnpfcxuw gqzumíqtxmy mi oqrg yreqvjyv bgm yy pwmug kytvitu; tpdw kmxz uuvivem xuws l zckmxca kayrea; jgmxl cck yr wm vglvloqót xép ya ak mewsi ah tfzbu xi wm dklhlp.'''

first = ord('a') #
last = ord('z')
L = last - first

bad_chars = [' ', ',', '.', ';']

def encode(message, key):
    message = message.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

    res = ''

    k = 0
    m = 0

    while m < len(message):

        if message[m] in bad_chars:
            res += message[m]
            m += 1
            continue

        a = ord(message[m]) - first
        b = ord(key[k]) - first

        ciph = a + b

        res += chr(first + ((ciph) % L))

        k = (k + 1) % len(key)
        m += 1

    return res

def decode(message, key):
    message = message.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

    res = ''

    k = 0
    m = 0

    while m < len(message):

        if message[m] in bad_chars:
            res += message[m]
            m += 1
            continue

        a = ord(message[m]) - first
        b = ord(key[k]) - first

        ciph = a - b

        res += chr(first + ((ciph) % L))

        k = (k + 1) % len(key)
        m += 1

    return res

key = ''
for i in range(len(msg)):
    for j in range(L):
        if encode(msg[i], chr(j + first)) == decode(msg[i], chr(j + first)):
            key += chr(j + first)
            break
# print(key)


passw = 'enunlugardelamanchadecuyonombrenoquieroacordarmenohamuchotiempoqueviviaunhidalgodelosdelanzaenastilleroadargaantiguarocinflacoygalgocorredorunaolladealgomasvacaquecarnerosalpiconlasmasnochesduelosyquebrantoslossabadoslentejaslosviernesalgunpalominodeanadiduralosdomingosconsumianlastrespartesdesuhacienda'

passw = 'miftekmiguelmigtelmiguekligtekmigtelmiguelligtelmiguekmigtelmigtellifauelmiguelligtekmiguekmiguekmiguelmigtelmigtekmiguaelmigtdlmigtelliguekligtelmiguelliagtelmifuelligtekmigtealmigtaelliguelligteklhguelmhgtellhaguelligtelmigtekligtelligtaekmigtelligugelmiftellhgtelmigtelmhftaelmigtelligtelligtelmiguelm'

deco = decode(msg, passw)
print(deco) # this is the password
for i in bad_chars:
    deco = deco.replace(i, '')
deco = decode(msg, deco)
# print(deco)
