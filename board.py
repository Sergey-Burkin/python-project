from pieces import *
from square import *


class Board:
    size = 10
    chosen = None
    cnt = {}

    def __init__(self, size=10):
        self.size = size
        self.board = [[Square() for _ in range(self.size)] for _ in
                      range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if (i + j) % 2 == 1:
                    self.board[i][j].color = Color.BLACK

    def print(self):
        for i in range(self.size):
            print(i, *self.board[i], i)

    def square_by_coordinate(self, n):
        return self.board[(n - 1) // 5][(n - 1) % 5 * 2 + 1 - (n - 1) // 5 % 2]

    def set_checkers(self):
        for i in range(1, 21):
            self.square_by_coordinate(i).figure = Men(Color.BLACK)
        for i in range(31, 51):
            self.square_by_coordinate(i).figure = Men(Color.WHITE)

    def get_square(self, position):
        return self.board[position[0]][position[1]]

    def is_valid(self, position):
        for i in range(2):
            if 0 > position[i] or self.size <= position[i]:
                return False
        return True

    def mark(self, position):
        self.get_square(position).figure.mark_the_squares(self, position)

    def can_eat(self, position):
        return self.get_square(position).figure.can_eat(self, position)

    def any_can_eat(self, color):
        for i in range(self.size):
            for j in range(self.size):
                if not self.get_square((i, j)).empty():
                    if self.can_eat((i, j)) and self.get_square(
                            (i, j)).figure.color == color:
                        return True
        return False

    def move(self, position_from, position_to):
        return self.get_square(position_from).figure.move(self, position_from,
                                                          position_to)

    def update_figures(self):
        for square in self.board[0]:
            if square.empty():
                continue
            if square.figure.color == Color.WHITE:
                square.figure = King(Color.WHITE)
        for square in self.board[-1]:
            if square.empty():
                continue
            if square.figure.color == Color.BLACK:
                square.figure = King(Color.BLACK)

    def get_the_number_of_pieces(self):
        result = {color: 0 for color in [Color.WHITE, Color.BLACK]}
        for line in self.board:
            for square in line:
                if not square.empty():
                    result[square.figure.color] += 1
        return result
