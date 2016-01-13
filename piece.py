import random

#SHAPE TUPLES
S_TEMPLATE = [[(2,2),(3,2),(2,3),(1,3)],
              [(2,1),(2,2),(3,2),(3,3)]]

Z_TEMPLATE = [[(1,2),(2,2),(2,3),(3,3)],
              [(2,1),(2,2),(1,2),(1,3)]]

I_TEMPLATE = [[(2,0),(2,1),(2,2),(2,3)],
              [(0,2),(1,2),(2,2),(3,2)]]

O_TEMPLATE = [[(1,2),(2,2),(1,3),(2,3)]]

J_TEMPLATE = [[(1,1),(1,2),(2,2),(3,2)],
              [(3,1),(2,1),(2,2),(2,3)],
              [(1,2),(2,2),(3,2),(3,3)],
              [(2,1),(2,2),(2,3),(1,3)]]

L_TEMPLATE = [[(3,1),(1,2),(2,2),(3,2)],
              [(3,3),(2,1),(2,2),(2,3)],
              [(1,2),(2,2),(3,2),(1,3)],
              [(2,1),(2,2),(2,3),(1,1)]]

T_TEMPLATE = [[(1,2),(2,2),(3,2),(2,1)],
              [(2,1),(2,2),(2,3),(3,2)],
              [(1,2),(2,2),(3,2),(2,3)],
              [(2,1),(2,2),(2,3),(1,2)]]

SHAPES = [S_TEMPLATE,Z_TEMPLATE,I_TEMPLATE,
          O_TEMPLATE,J_TEMPLATE,
          L_TEMPLATE,T_TEMPLATE]

class Piece:
    def __init__(self, color):
        self.color = color
        self.shape = random.randrange(0,len(SHAPES),1)
        self.rotation = random.randrange(0,len(SHAPES[self.shape]))
        self.coord = [2,-3]

    def get_board_coord(self):
        board_coord = []

        for tuple in SHAPES[self.shape][self.rotation]:
            new_tuple = (tuple[0]+self.coord[0], tuple[1]+self.coord[1])
            board_coord.append(new_tuple)

        return board_coord

    def get_color(self):
        return self.color

    def get_shape(self):
        return SHAPES[self.shape]

    def rotate(self, dir):
        self.rotation = (self.rotation + dir) % len(SHAPES[self.shape])

    def reset_coord(self):
        self.coord = [2,-3]

    def shift(self, dir):
        self.coord[0]+=dir

