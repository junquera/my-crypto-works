import random

MAX = 1024*2
tree = {}

for i in range(MAX):
    random.seed(i)
    
    tree[i] = {}

    last = random.randint(0, MAX)
    
    for _ in range(MAX):
        n = random.randint(0, MAX)
        if last in tree[i]:
            tree[i][last].append(n) 
        else:
            tree[i][last] = [n]

        last = n
    
candidates = tree.keys()
last = -1
while len(candidates) > 1:
    
    reto = int(input('N > '))
    
    next_candidates = [] 
    for x in candidates:
        if reto in tree[x].keys():
            if last >= 0:
                if reto in tree[x][last]:
                    next_candidates.append(x)
            else:
                    next_candidates.append(x)

    candidates = next_candidates
    last = reto

print(candidates)
