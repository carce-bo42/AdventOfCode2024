
# The ones digit of a number is the digit in the rightmost position of the number.
# It represents the remainder when the number is divided by 10. For example:

from collections import defaultdict, deque

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

def gather_all_merchant_prices(secrets: list[int]) -> dict[tuple[int], int]:

    prices = defaultdict(int)
    for secret in secrets:

        last_prices_gradient = deque()
        keys_added = set()

        # Do first iteration
        for i in range(4):
            last_secret = secret
            secret = get_next_secret(secret)
            last_prices_gradient.append((secret%10)-(last_secret%10))

        key = tuple(last_prices_gradient)
        prices[key] += secret%10
        keys_added.add(key)

        # Keep track of all prices for all diff vectors.
        for i in range(4,2000):

            last_secret = secret
            secret = get_next_secret(secret)

            last_prices_gradient.append((secret%10)-(last_secret%10))
            last_prices_gradient.popleft()

            key = tuple(last_prices_gradient)
            if key not in keys_added:
                prices[key] += secret%10
                keys_added.add(key)

    return prices


if __name__ == "__main__":

    secrets = read_file("input.txt")
    prices = gather_all_merchant_prices(secrets)
    print(max(prices.values()))