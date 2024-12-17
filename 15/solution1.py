# X_LEN = 50
# Y_LEN = 50
X_LEN = 50
Y_LEN = 50

class _Map:

    def __init__(self, x_len = X_LEN, y_len = Y_LEN):

        self.x_len = x_len
        self.y_len = y_len
        self._map = [['.'] * x_len for _ in range(y_len)]

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
        rows_as_strings = [" ".join(map(str, row)) for row in self._map]
        return "\n".join(rows_as_strings)

    def compute_gps_coordinates(self):

        gps_coordinates = 0
        for x in range(0, self.x_len):
            for y in range(0, self.y_len):
                if _map[x,y] == 'O':
                    gps_coordinates += (y * 100) + x

        return gps_coordinates

class Robot():

    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def push_boxes(self, _map, direction):

        dx, dy = direction_vectors[direction]

        xinc = dx
        yinc = dy

        # Seek pos at end of O sequence
        while _map[self.x + xinc, self.y + yinc] == 'O':
            xinc += dx
            yinc += dy
        #print(f"xinc={xinc}, yinc={yinc}")

        # If the O sequence ends in a wall, do nothing.
        if _map[self.x + xinc, self.y + yinc] == '#':
            return
        else:
            # put a new O at end of O sequence.
            _map[self.x + xinc, self.y + yinc] = 'O'
            # position robot at start of O sequence,
            _map[self.x, self.y] = '.'
            self.x += dx
            self.y += dy
            _map[self.x, self.y] = '@'


direction_vectors = {
    '^' : (0,-1),
    '>' : (+1,0),
    'v' : (0,+1),
    '<' : (-1,0)
}

def process_instructions(rob, _map, sline):

    for direction in sline:

        dx, dy = direction_vectors[direction]
        obj = _map[rob.x + dx, rob.y + dy]

        if obj == '#':
            continue
        elif obj == '.':
            _map[rob.x, rob.y] = '.'
            _map[rob.x+dx, rob.y+dy] = '@'
            rob.x += dx
            rob.y += dy
        else:
            #print(f"pushing boxes at direction {direction}")
            rob.push_boxes(_map, direction)


fname = "input.txt"
# _map[x][y] = (x,y)
_map = _Map()
end_parse_map = False
with open(fname) as file:
    for y, line in enumerate(file):
        sline = line.strip()
        if len(sline) == 0:
            end_parse_map = True
            continue
        if not end_parse_map:
            for x, char in enumerate(sline):
                _map[x,y] = char
                if char == '@':
                    rob = Robot(x, y)
                    # Erase position from map
        else:
            process_instructions(rob, _map, sline)

print(_map)
print(_map.compute_gps_coordinates())

