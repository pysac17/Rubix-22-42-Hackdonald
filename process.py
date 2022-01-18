import json

opens=open(r"C:\Users\arjun\Desktop\rizfood (1).json")
reads=opens.read()
loads=json.loads(reads)

ingredient = ['tomato', 'cheese', 'milk','bread']
length = len(ingredient)
confirm = [x*0 for x in range(length)]
indexes = [str(x+1) for x in range(596)]
totals = [x*0 for x in range(len(indexes))]
fin = ""

for i in range(596):
    for k in range(length):
        for j in range(len(loads[indexes[i]]['ingredients'])):
            if ingredient[k] in loads[indexes[i]]['ingredients'][j]:
                confirm[k] = 1
    total = 0
    for a in range(length):
        total = total + confirm[a]
    totals[i] = total
    for b in range(length): confirm[b] = 0
    
max = 0
for l in range(596):
    if totals[l]>max: max = totals[l]

for m in range(max):
    for n in range(596):
        if totals[n] == max:
            fin = fin + str(n + 1) + '.'
    max = max - 1

print(fin)