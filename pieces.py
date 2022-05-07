import pygame
from graphic import Color, BLACK_KING_COLOR, BLACK_MEN_COLOR, WHITE_KING_COLOR, \
    WHITE_MEN_COLOR, crown, crown_rect

INF = 10000


def next_color(color):
    if color == Color.WHITE:
        return Color.BLACK
    return Color.WHITE


class Figure:
    color = Color.WHITE

    def move(self, board, position_from,
             position_to):  # return the color of next turn
        result = next_color(self.color)
        board.get_square(position_to).figure = board.get_square(
            position_from).figure
        for current_position in get_intermediate_positions(position_from,
                                                           position_to):
            if not board.get_square(current_position).empty():
                if board.get_square(
                        current_position).figure.color != self.color:
                    result = self.color
            board.get_square(current_position).figure = None
        return result


def add_vector_to_point(point, vector, n=1):
    result = [0, 0]
    for i in range(2):
        result[i] = point[i] + vector[i] * n
    return result


def get_vector(position_from, position_to):
    vector = [position_to[0] - position_from[0],
              position_to[1] - position_from[1]]
    n = abs(vector[0])
    vector[1] //= n
    vector[0] //= n
    return vector


def get_intermediate_positions(position_from, position_to):
    vector = get_vector(position_from, position_to)
    n = abs(position_to[0] - position_from[0])
    return [(add_vector_to_point(position_from, vector, i)) for i in range(n)]


def get_center_position(position, square_width, square_height):
    return position[0] + square_width // 2, position[1] + square_height // 2


def get_radius(square_width, square_height):
    return min(square_width, square_height) * 3 // 7


class Men(Figure):
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, color):
        self.color = color

    def get_image(self):
        if self.color == Color.WHITE:
            return '⛀'
        else:
            return '⛂'

    def can_eat(self, board, my_position, mark_squares=False):
        result = False
        for direction in self.directions:
            next_position = add_vector_to_point(my_position, direction, 1)
            next_to_position = add_vector_to_point(my_position, direction, 2)
            if not board.is_valid(next_position) or not board.is_valid(
                    next_to_position):
                continue
            square = board.get_square(next_position)
            next_square = board.get_square(next_to_position)
            if not square.empty() and square.figure.color != self.color and next_square.empty():
                if mark_squares:
                    next_square.beaten = True
                result = True
        return result

    def mark_the_squares(self, board, my_position):
        if self.can_eat(board, my_position, True):
            return
        if self.color == Color.BLACK:
            forward_directions = self.directions[0:2]
        else:
            forward_directions = self.directions[2:4]
        for direction in forward_directions:
            next_position = add_vector_to_point(my_position, direction)
            if not board.is_valid(next_position):
                continue
            the_square = board.get_square(next_position)
            if the_square.empty():
                the_square.beaten = True

    def get_py_color(self):
        if self.color == Color.WHITE:
            return WHITE_MEN_COLOR
        if self.color == Color.BLACK:
            return BLACK_MEN_COLOR

    def draw(self, win, position, square_width, square_height):
        center = get_center_position(position, square_width, square_height)
        radius = get_radius(square_width, square_height)
        pygame.draw.circle(win, self.get_py_color(), center,
                           radius)


def get_possible_position(board, my_position, direction):
    result = []
    for i in range(1, INF):
        position = add_vector_to_point(my_position, direction, i)
        if not board.is_valid(position):
            break
        if not board.get_square(position).empty():
            break
        result.append(position)
    return result


class King(Figure):
    directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

    def get_image(self):
        if self.color == Color.WHITE:
            return '⛁'
        else:
            return '⛃'

    def __init__(self, color=Color.WHITE):
        self.color = color

    def can_eat(self, board, my_position):
        for direction in self.directions:
            for i in range(1, INF):
                new_position = add_vector_to_point(my_position, direction, i)
                next_position = add_vector_to_point(my_position, direction,
                                                    i + 1)
                if not (board.is_valid(new_position) and board.is_valid(
                        next_position)):
                    break
                current_square = board.get_square(new_position)
                next_square = board.get_square(next_position)
                if current_square.empty():
                    continue
                if current_square.figure.color == self.color:
                    continue
                if next_square.empty():
                    return True
                break

        return False

    def mark_the_squares(self, board, my_position):
        if not self.can_eat(board, my_position):
            for direction in self.directions:
                for position in get_possible_position(board, my_position,
                                                      direction):
                    board.get_square(position).beaten = True
            return
        for direction in self.directions:
            for i in range(1, INF):
                position = add_vector_to_point(my_position, direction, i)
                if not board.is_valid(position):
                    break
                current_square = board.get_square(position)
                if current_square.empty():
                    continue
                if current_square.figure.color == self.color:
                    break
                other_figure = current_square.figure
                current_square.figure = None
                board.get_square(my_position).figure = None
                can_beat_after = False
                possible_position = get_possible_position(board, position,
                                                          direction)
                for new_position in possible_position:
                    if self.can_eat(board, new_position):
                        board.get_square(new_position).beaten = True
                        can_beat_after = True
                if not can_beat_after:
                    for new_position in possible_position:
                        board.get_square(new_position).beaten = True
                current_square.figure = other_figure
                board.get_square(my_position).figure = self

    def get_py_color(self):
        if self.color == Color.WHITE:
            return WHITE_KING_COLOR
        if self.color == Color.BLACK:
            return BLACK_KING_COLOR

    def draw(self, win, position, square_width, square_height):
        center = get_center_position(position, square_width, square_height)
        radius = get_radius(square_width, square_height)
        pygame.draw.circle(win, self.get_py_color(), center,
                           radius)
        crown_rect.center = center

        win.blit(crown, crown_rect)
