X_LEN = 100
Y_LEN = 50

class _Map:

    def __init__(self, x_len = X_LEN, y_len = Y_LEN):

        self.x_len = x_len
        self.y_len = y_len
        self.__map = [['.'] * x_len for _ in range(y_len)]

    def __getitem__(self, indices):
        """
        Allow access using instance[x, y] where x is column and y is row.
        """
        if isinstance(indices, tuple) and len(indices) == 2:
            x, y = indices
            return self.__map[y][x]
        else:
            raise IndexError("Invalid index format. Use [x, y] to access elements.")

    def __setitem__(self, indices, value):
        """
        Allow setting values using instance[x, y] where x is column and y is row.
        """
        if isinstance(indices, tuple) and len(indices) == 2:
            x, y = indices
            self.__map[y][x] = value
        else:
            raise IndexError("Invalid index format. Use [x, y] to set elements.")

    def __repr__(self):
        rows_as_strings = ["".join(map(str, row)) for row in self.__map]
        return "\n".join(rows_as_strings)

    def compute_gps_coordinates(self):

        gps_coordinates = 0
        for x in range(0, self.x_len):
            for y in range(0, self.y_len):
                if self.__map[x,y] == 'O':
                    gps_coordinates += (y * 100) + x

        return gps_coordinates

    # xbox, ybox ALWAYS point towards the left side of a box, '['
    def boxes_can_be_moved(self, xbox, ybox, dy, memo):

        # Do not process boxes that have already been processed.
        if (xbox, ybox) in memo:
            return True

        memo.add((xbox,ybox))

        # There is a wall on the direction
        if self[xbox, ybox+dy] == '#' or self[xbox+1,ybox+dy] == '#':
            return False

        # There is space to move the box in the direction
        if self[xbox, ybox+dy] == '.' and self[xbox+1,ybox+dy] == '.':
            return True

        # Box is aligned
        if self[xbox, ybox+dy] == '[':
            return self.boxes_can_be_moved(xbox, ybox+dy, dy, memo)

        # Case we go wide. This is potentially redundant since:
        #[][][]
        # [][]  -> The top middle box would be checked twice => we use memo.
        #  []
        #
        if self[xbox, ybox+dy] == ']' and self[xbox+1,ybox+dy] == '[':
            return self.boxes_can_be_moved(xbox-1,ybox+dy,dy,memo) and self.boxes_can_be_moved(xbox+1,ybox+dy,dy,memo)

        if self[xbox, ybox+dy] == ']':
            return self.boxes_can_be_moved(xbox-1,ybox+dy,dy,memo)

        if self[xbox+1,ybox+dy] == '[':
            return self.boxes_can_be_moved(xbox+1,ybox+dy,dy,memo)

    def compute_gps_coordinates(self):

        gps_coordinates = 0
        for x in range(0, self.x_len):
            for y in range(0, self.y_len):
                if _map[x,y] == '[':
                    gps_coordinates += (y * 100) + x

        return gps_coordinates

class Robot():

    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def push_big_boxes(self, _map, direction):

        dx, dy = direction_vectors[direction]

        if dy == 0:
            xinc = dx
            box_sides = ('[',']')
            bidx = 0 if _map[self.x + xinc, self.y] == '[' else 1

            while _map[self.x + xinc, self.y] == box_sides[bidx]:
                xinc += 2*dx

            if _map[self.x + xinc, self.y] == '#':
                return
            else:
                _map[self.x, self.y] = '.'
                self.x += dx
                _map[self.x, self.y] = '@'

                # move all boxes to the right/left
                _dx = dx
                while _dx != xinc:
                    _map[self.x + _dx, self.y] = box_sides[bidx]
                    _map[self.x +_dx + dx, self.y] = box_sides[(bidx+1)%2]
                    _dx += 2*dx
        else:
            # Box pos points to '[', independently of the position
            # of the robot.
            if _map[self.x, self.y+dy] == ']':
                box = (self.x-1, self.y+dy)
            else:
                box = (self.x, self.y+dy)

            memo = set()
            if _map.boxes_can_be_moved(*box, dy, memo):

                # push boxes
                memo = set()
                self.do_push(_map, *box, dy, memo)

                # move robot
                _map[self.x, self.y] = '.'
                self.y += dy
                _map[self.x, self.y] = '@'


    def do_push(self, _map, xbox, ybox, dy, memo):

        if (xbox,ybox) in memo:
            return

        memo.add((xbox,ybox))

        _map[xbox,ybox] = '.'
        _map[xbox+1,ybox] = '.'

         # There is space to move the box in the direction
        if _map[xbox, ybox+dy] == '.' and _map[xbox+1,ybox+dy] == '.':
            _map[xbox, ybox+dy] = '['
            _map[xbox+1, ybox+dy] = ']'
            return

        if _map[xbox, ybox+dy] == '[':
            self.do_push(_map, xbox, ybox+dy, dy, memo)
            _map[xbox, ybox+dy] = '['
            _map[xbox+1, ybox+dy] = ']'
            return

        if _map[xbox, ybox+dy] == ']':
            self.do_push(_map, xbox-1, ybox+dy, dy, memo)

        if _map[xbox+1, ybox+dy] == '[':
            self.do_push(_map, xbox+1, ybox+dy, dy, memo)

        _map[xbox, ybox+dy] = '['
        _map[xbox+1, ybox+dy] = ']'
        return

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
            rob.push_big_boxes(_map, direction)


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
                if char == 'O':
                    _map[2*x,y] = '['
                    _map[2*x+1,y] = ']'
                elif char == '@':
                    rob = Robot(2*x, y)
                    _map[2*x,y] = '@'
                elif char == '#':
                    _map[2*x,y] = '#'
                    _map[2*x+1,y] = '#'
        else:
            process_instructions(rob, _map, sline)

print(_map.compute_gps_coordinates())