#m = "HEEINOSSLCLTRFEAOAE"

m = input("Cipher text > ")

for i in range(len(m))[1:10]:
    possibilities = [[] for _ in range(i)]
    for j in range(len(m)):
        possibilities[j%len(possibilities)].append(m[j])
    
    res = "".join(["".join(x) for x in possibilities])
    print("[%02d] %s" % (i, res))
