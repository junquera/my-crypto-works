phrase = 'en un lugar de la mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivia un hidalgo de los de lanaa en astillero, adarga antigua, rocin flaco y galgo corredor. una olla de algo mas vaca que carnero, salpicon'

bad_chars = [' ', ',', '.', ';']

res = ''
for i in phrase:
  if i in bad_chars:
    res += i
  else:
    res += '.'

print("This is the pattern for your phrase:\n%s" % res)
