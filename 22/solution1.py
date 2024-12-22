prune_mask = 0xffffff

# The "ones digit" is, at most, 9, at least, 0.:
# 0000, 0001, 0010, 0011, 0100, 0101, 0110, 0111, 1000, 1001 | 1010 -> this ones digit is 0.
# So we only care about the last 3 binary digits.
def get_next_secret(secret: int):

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


if __name__ == "__main__":

    secrets = read_file("input.txt")
    total = 0
    for secret in secrets:
        for i in range(2000):
            secret = get_next_secret(secret)
        total += secret
    print(total)