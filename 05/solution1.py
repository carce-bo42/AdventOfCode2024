#Arguably se podría hacer un procesado de las reglas con un diccionario
# Algo como { "numeros izq" : [ numeros derecha ] }.
# Pero esta solucion de sustituir los , por | y hacer comparaciones no
# me parece tampoco fea.

import regex as re

fname = "input.rules.txt"
rules = []
with open(fname) as file:
    for line in file:
        rules.append(line.strip())

        
fname = "input.txt"
count = 0 
with open(fname) as file:
    for line in file:
        upd = line.strip().replace(",", "|")
        valid_update = True
        for match in re.findall(r"\d{2}\|\d{2}", upd, overlapped=True):
            if match not in rules:
                valid_update = False
                break
        if valid_update:
            ll = upd.strip().split("|")
            count += int(ll[len(ll)//2])
            
print(count)