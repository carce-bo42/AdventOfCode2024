
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


def read_file(filename: str) -> list[int]:

    secrets = []
    with open(filename) as file:
        for line in file:
            secrets.append(int(line.strip()))

    return secrets


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