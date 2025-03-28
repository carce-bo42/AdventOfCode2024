#Arguably se podría hacer un procesado de las reglas con un diccionario
# Algo como { "numeros izq" : [ numeros derecha ] }.
# Pero esta solucion de sustituir los , por | y hacer comparaciones no
# me parece tampoco fea.

import regex as re

def test_solution(upd):
    for match in re.findall(r"\d{2}\|\d{2}", upd, overlapped=True):
        if match not in rules_list:
            return False
    return True

def test_solution_with_log(upd):
    for match in re.findall(r"\d{2}\|\d{2}", upd, overlapped=True):
        if match not in rules_list:
            print(f"Mira este match está mal: {match}")
            return False
    return True

def reduced_list(lst, number):
    return [ item for item in lst if item != number ]

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def find_best_value(start, _pool, choices, solution, _len):
    
    solution.append(start)
    
    # print(f"start : {start}")
    # print(f"Solution: {solution}")
    # print(f"Choices: {choices}")
    # print(f"pool:  {_pool}")

    # print("--------------------------------")
    
    # Si ya tenemos una solucion valida
    if len(solution) == _len:
        return True, solution
    
    # Si no hay ninguna posibilidad
    if start not in rules_dict.keys():
        return False, []

    if len(choices) == 0:
        return False, []
    
    if len(intersection(choices, _pool)) == 0:
        return False, []
    
    for y in choices:
        # Las nuevas posibilidades son las que hayan en el diccionario que coincidan
        # con valores que no están ya quitados del pool
        ok, result = find_best_value(
            y,
            reduced_list(_pool, y),
            [ item for item in reduced_list(_pool, y) if item in rules_dict[y] ],
            solution,
            _len
        )
        if ok:
            return True, result
        else:
            solution.pop()
    return False, []

fname = "input.rules.txt"
rules_list = []
with open(fname) as file:
    for line in file:
        rules_list.append(line.strip())

fname = "input.txt"
upd_to_fix = []
with open(fname) as file:
    for line in file:
        upd = line.strip().replace(",", "|")
        if not test_solution(upd):
            upd_to_fix.append(upd)

# Hay que hacer un arbol con las posibilidades correctas que hay
# Al final el diccionario es un must
rules_dict = {}
for rule in rules_list:
    pair = rule.split("|")
    rules_dict.setdefault(pair[0], [])
    rules_dict[pair[0]].append(pair[1])

count = 0
for upd in upd_to_fix:
    pool = upd.split("|")
    # Empezamos a iterar. Hay que probar que todos los numeros puedan
    # ser el primero e ir haciendo
    solution = []
    for x in pool:
        solution = []
        # Filtramos en funcion de las posibilidades validas
        ok, result = find_best_value(
            x,
            reduced_list(pool, x),
            [ item for item in reduced_list(pool, x) if item in rules_dict[x] ],
            solution,
            len(pool)
        )
        if ok:
            count += int(solution[len(solution)//2])
            break
        
print(count)