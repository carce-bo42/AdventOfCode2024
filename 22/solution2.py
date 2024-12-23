
# The ones digit of a number is the digit in the rightmost position of the number.
# It represents the remainder when the number is divided by 10. For example:
 
from functools import cache

prune_mask = 0xffffff

# The "ones digit" is, at most, 9, at least, 0.:
# 0000, 0001, 0010, 0011, 0100, 0101, 0110, 0111, 1000, 1001 | 1010 -> this ones digit is 0.
# So we only care about the last 3 binary digits.
def get_next_secret(secret: int) -> int:

    secret = ((secret << 6) ^ secret) & prune_mask
    secret = ((secret >> 5) ^ secret) & prune_mask
    secret = ((secret << 11) ^ secret) & prune_mask

    return secret


def enumerate_quads(lst: list[int]):
    
    if len(lst) < 4:
        return lst
    
    for pos, _ in enumerate(lst):
        if pos+3 == len(lst)-1:
            break
        yield pos, lst[pos], lst[pos+1], lst[pos+2], lst[pos+3]


def read_file(filename: str) -> list[int]:

    secrets = []
    with open(filename) as file:
        for line in file:
            secrets.append(int(line.strip()))

    return secrets

# El plan:
# Para cada matriz de precios:
# 1. Encontrar los 9 y sacarles la secuencia de diferencias.
# 2. Filter out las secuencias que sucedan antes que ellos.
# 3 Añadir esas secuencias al total de secuencias que queremos probar.
# Calcular el valor asociado a cada uno de estas.
# Esto no es computacionalmente complejo, pero pide mucha mucha memoria.
# Tenemos que tener 1 diccionario de ~2k key-values por cada comerciante

# 1 lista de ~1800 diccionarios, cada uno con ~2k valores ~ 1.8k * 2k ~ 400MB

# El problema de hacerlo dinámico es que si en la enesima iteracion encuentras una secuencia,
# y es la buena, tienes que poder volver atrás para comprobar que funciona ese quad.

# Nos basta con una lista de tuplas. [0] = price [1] = difference. 

def gather_all_merchant_prices(secrets: list[int]) -> list[tuple[tuple[tuple[int,int]], set[int]]]:
    
    merchants = []
    for secret in secrets:
        
        price_diff = [(secret%10, None)]   
        candidates = set()
        for i in range(2000):
            secret = get_next_secret(secret)
            price = secret%10
            price_diff.append((price, price - price_diff[-1][0]))
            if price == 9 and i+1 > 3:
                candidates.add(i+1)
        
        merchants.append((tuple(price_diff),candidates))
        
    return merchants

@cache
def get_idx_of_first_occurence(
        sequence: tuple[int, int, int, int],
        diffs: tuple[int]
    )-> int:

    for idx, a, b, c, d in enumerate_quads(diffs):
        if (a,b,c,d) == sequence:
            return idx

def filter_candidates(
        merchants: list[tuple[list[tuple[int,int]], list[int]]]
    ) -> list[tuple[int,int,int,int]]:
    
    for m in merchants:
        true_candidates = []
        price_diff, candidates = m
        print(f"total initial candidates{len(candidates)}")
        for cnd in candidates:
            sequence = (
                price_diff[cnd-3][1],
                price_diff[cnd-2][1],
                price_diff[cnd-1][1],
                price_diff[cnd][1]
            )
            idx = get_idx_of_first_occurence(sequence, tuple(x[1] for x in price_diff))
            #print(idx, cnd-3)
            if idx == cnd-3:
                true_candidates.append(sequence)
    
    return true_candidates
                
    

if __name__ == "__main__":

    secrets = read_file("input.txt")
    merchants = gather_all_merchant_prices(secrets)
    candidates = filter_candidates(merchants)
    print(f"total candidates = {len(candidates)}")
    