import sys

alfabetoMay = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S','T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alfabetoMin = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def main(argv = sys.argv):
    num = int(argv[1])
    palabra = raw_input("> ")
    print calcula(num, palabra)

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
            resultado+=i
    return resultado

def isMay(letra):
    return letra == letra.upper()

if __name__ == "__main__":
    sys.exit(main())

