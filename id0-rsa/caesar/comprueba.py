import cesar
import sys
def main():
    palabra = raw_input("> ")
    for i in range(len(cesar.alfabetoMay)):
        print(str(len(cesar.alfabetoMay) - i) +"\t" + str(cesar.calcula(i, palabra)))
if __name__ == "__main__":
    sys.exit(main())
