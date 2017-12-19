import sys

alfabetoMay = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S','T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alfabetoMin = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def main(argv = sys.argv):
    num = int(argv[1])
    # palabra = input("> ")
    palabra = '''Rpnd Yjaxd Réhpg, fjt th jcd st adh igth báh vgpcsth rpexipcth st ap Wxhidgxp rdc Patypcsgd Bpvcd n rd
c Cpedatóc, th ipbqxéc jcd st adh igth báh rdchxstgpqath wxhidgxpsdgth apixcdh, rdc Rpnd Rgxhed Hpajhixd n rdc Ixid Axkxd, udgbpcsd ta tytbeapg igxjckxgpid sta etgídsd raáhxrd edg tmrtatcrxp
, etgídsd ktgspstgpbtcit «ájgtd» st aph atigph apixcph.

Hx wph advgpsd aatvpg wphip pfjí, ij gtrdbetchp htgá ap st hpqtg fjt ap rdcigphtñp epgp hjetgpg thit gtid th Ratdepigp. N Yjaxd Réhpg th idsd thid, ixtct ipa hxvcxuxrprxóc, egtrxhpbtcit rdbd
 wxhidgxpsdg st hí bxhbd, cpggpsdg st hjh egdexph wpopñph vjtggtgph n st hj edaíixrp.'''
    print(calcula(num, palabra))

def calcula(num, palabra):
    resultado = ''
    for i in palabra:
        if i == ' ':
            resultado += ' '
            continue

        contador = 0
        exito = False

        alfabeto = alfabetoMay if isMay(i) else alfabetoMin

        for j in alfabeto:
            if i == j:
                if (contador - num) >= len(alfabeto):
	                resultado += alfabeto[(contador - num) % len(alfabeto)]
                else:
                    resultado += alfabeto[contador - num]
                    exito = True
                break
            contador+=1
        if not exito:
            resultado += i
    return resultado

def isMay(letra):
    return letra == letra.upper()

if __name__ == "__main__":
    sys.exit(main())
