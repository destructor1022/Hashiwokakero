import math
import random

class Hashi:
    class Piece:
        def __init__(self, struct = "closed", val = 0):
            self.struct = struct
            self.val = val
        
        def __str__(self):
            return str(self.struct) + "," + str(self.val)

        def __eq__(self, other):
            return self.struct is other.struct and self.val == other.val

        def change_to(self, new_struct, new_val):
            self.struct = new_struct
            self.val = new_val
        
        def increment(self):
            self.val += 1

    def __init__(self, width, height):
        self.board = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(self.Piece())
            self.board.append(row)
        self.node_list = []

    def width(self):
        return len(self.board[0])
    
    def height(self):
        return len(self.board)

    def coord_to_pos(self, coord):
        pos = [math.floor(len(self.board) - coord[1]), math.floor(coord[0])]
        return pos

    def get(self, coord):
        pos = self.coord_to_pos(coord)
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.height() - 1 or pos[1] > self.width() - 1:
            raise Exception("not in bounds")
        return self.board[pos[0]][pos[1]]
    
    def alter(self, coord, struct = None, val = None):
        curr = self.get(coord)
        if struct is None:
            struct = curr.struct
        if val is None:
            val = curr.val
        curr.change_to(struct, val)
        if struct == "node":
            self.node_list.append(coord)
        
    def gen_ellipse_grid(self):
        # inside of ellipse: ((x - (w/2))^2/(w/2)^2)+((y - (h/2))^2/(h/2)^2)<=1
        width = self.width()
        height = self.height()

        def inside_ellipse(coord):
            to_check = []
            funcs = [math.floor, math.ceil]
            for i in funcs:
                for j in funcs:
                    to_check.append([i(coord[0]), j(coord[1])])

            for curr in to_check:
                norm_dist = (curr[0] - width/2)**2 / (width/2)**2 + (curr[1] - height/2)**2 / (height/2)**2
                inside = 1 >= norm_dist
                if inside is False:
                    return False
        
            return True

        for i in range(width):
            for j in range(height):
                curr = [i + 0.5, j + 0.5]
                if inside_ellipse(curr) is True:
                    self.alter(curr, "open")

    def gen_rect_grid(self):
        for i in range(self.width()):
            for j in range(self.height()):
                curr = [i + 0.5, j + 0.5]
                self.alter(curr, "open")

    def grid_str(self, type = None):
        string = ""
        for i in self.board:
            for j in i:
                if type == "debug":
                    string += str(j)
                    string += ";"
                elif type == "solved":
                    if j.struct == "bridge":
                        string += "+"
                    else:
                        if j.val > 0:
                            string += str(j.val)
                        else:
                            string += " "
                else:
                    if j.val > 0:
                        string += str(j.val)
                    else:
                        string += " "
            string += "\n"
        return string

    def compare(self, coord1, coord2 = None, struct = None, val = None):
        if coord2 is None:
            if struct is None:
                return self.get(coord1).val == val
            elif val is None:
                return self.get(coord1).struct == struct
            return self.get(coord1) == self.Piece(struct, val)
        elif struct is None or val is None:
            return self.get(coord1) == self.get(coord2)
        raise Exception("not enough argements")

    def get_rand_pos(self, struct = "open", val = 0):
        for loops in range(50):
            rand_coord = [
                random.randint(0, self.width() - 1) + 0.5, 
                random.randint(0, self.height() - 1) + 0.5
            ]
            if self.compare(rand_coord, struct = struct, val = val):
                return rand_coord
        raise Exception("no points available")

    def create_first(self, struct = "node", val = 0):
        self.alter(self.get_rand_pos("open", 0), struct, val)

    
    def increment(self, coord):
        pos = self.coord_to_pos(coord)
        self.board[pos[0]][pos[1]].increment()

    def find_line_pos(self, start_coord, direction = 0, movement = 1):
        # {left: (d = 0, m = 1), up: (d = 1, m = 1), right: (d = 0, m = -1), down: (d = 1, m = -1)}
        available = []
        move_coord =  [start_coord[0], start_coord[1]]   
        while True:
            try:
                move_coord[direction] += movement
                curr = [move_coord[0], move_coord[1]]
                if self.compare(curr, struct = "open", val = 0) is True:
                    available.append(curr)
                elif self.compare(curr, struct = "node") is True:
                    available.append(curr)
                    break
                else:
                    break
            except:
                break
        return available

    def build_bridge(self, start_coord, available):
        first = available.pop(0)
        last = random.choice(available)
        available.insert(0, first)
        self.alter(last, "node")
        self.increment(last)
        for i in available:
            if i is last:
                break
            self.alter(i, "bridge")
        self.increment(start_coord)

    def build_random_bridge(self):
        built_bridge = False
        for loops in range(50):
            try:
                d = random.choice([0, 1])
                m = random.choice([-1, 1])
                start_coord = random.choice(self.node_list)
                avail = self.find_line_pos(start_coord, d, m)
                self.build_bridge(start_coord, avail)
                built_bridge = True
                break
            except:
                continue
        if built_bridge is False:
            raise Exception("bridge not built")

    def easy_game(self, shape, node_count = None):
        if shape == "ellipse":
            self.gen_ellipse_grid()
        else:
            self.gen_rect_grid()
        self.create_first()
        if node_count is None:
            while True:
                try:
                    self.build_random_bridge()
                except:
                    break
        elif node_count > 1:
            for loops in range(node_count - 1):
                try:
                    self.build_random_bridge()
                except:
                    break
        