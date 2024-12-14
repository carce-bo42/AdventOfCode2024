import re
import sys

X_LEN = 101
Y_LEN = 103

# Esto es para no volvernos locos ya que no está coordenado
# como normalmente lo están los arrays
class _Map:

    def __init__(self, x_len = X_LEN, y_len = Y_LEN):

        self.x_len = x_len
        self.y_len = y_len
        self._map = [[0] * x_len for _ in range(y_len)]

    def __getitem__(self, indices):
        """
        Allow access using instance[x, y] where x is column and y is row.
        """
        if isinstance(indices, tuple) and len(indices) == 2:
            x, y = indices
            return self._map[y][x]
        else:
            raise IndexError("Invalid index format. Use [x, y] to access elements.")

    def __setitem__(self, indices, value):
        """
        Allow setting values using instance[x, y] where x is column and y is row.
        """
        if isinstance(indices, tuple) and len(indices) == 2:
            x, y = indices
            self._map[y][x] = value
        else:
            raise IndexError("Invalid index format. Use [x, y] to set elements.")

    def __repr__(self):
        rows_as_strings = ["".join(map(str, [ '.' if v == 0 else v for v in row ])) for row in self._map]
        return "\n".join(rows_as_strings)

    def get_safety_factor(self):

        q1 = q2 = q3 = q4 = 0
        for x in range(0, self.x_len):
            for y in range(0, self.y_len):
                if x == (self.x_len // 2) or y == (self.y_len // 2):
                    continue
                if _map[x,y] == 0:
                    continue
                if x < (self.x_len // 2) and y < (self.y_len // 2):
                    q1 += _map[x,y]
                elif x > (self.x_len // 2) and y < (self.y_len // 2):
                    q2 += _map[x,y]
                elif x < (self.x_len // 2) and y > (self.y_len // 2):
                    q3 += _map[x,y]
                else:
                    q4 += _map[x,y]

        return q1 * q2 * q3 * q4

    def all_numbers_are_one(self):

        for x in range(0, self.x_len):
            for y in range(0, self.y_len):
                if _map[x,y] not in {0, 1}:
                    return False
        return True


# Es un torus. Abajo esta unido por arriba, y a la derecha con la izq.
# Está coordenado tal que:
# (0, 0) --- x + k ----> (k, 0)
#   |
#   |
# y + k
#   |
#   |
#   v
# (0, k)

# Si un punto (x, y) lo muevo en una direccion (X,Y) k veces:
# El punto acaba en (x+kX,y+kY).
# Luego hay que traducirlo dentro del mapa. Esta accion sobre el
# punto (x,y) lo traslará al punto:
# ((x+kX)mod(X_LEN),(x+kY)mod(Y_LEN))
# que está sobre el torus

fname = "input.txt"
# _map[x][y] = (x,y)
_map = _Map()
seconds = 100 if sys.argv[1] is None else int(sys.argv[1])
with open(fname) as file:
    for line in file:
        sline = line.strip()
        m = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", sline)
        p = (int(m.group(1)), int(m.group(2)))
        v = (seconds * int(m.group(3)), seconds * int(m.group(4)))
        p_final = ((p[0]+v[0])%X_LEN, ((p[1]+v[1])%Y_LEN))
        _map[*p_final] += 1

if _map.all_numbers_are_one():
    print(_map)