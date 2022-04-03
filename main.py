class Color(object):
    BLACK = 0
    WHITE = 1


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
                if board.get_square(current_position).figure.color != self.color:
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


class Men(Figure):
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, color):
        self.color = color

    def get_image(self):
        return ['⛂', '⛀'][self.color == Color.WHITE]

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
        return ['⛃', '⛁'][self.color == Color.WHITE]

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

    def mark_the_cells(self, board, my_position):
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


class Square:
    color = Color.WHITE
    figure = None
    beaten = False

    def empty(self):
        return self.figure is None

    def get_image(self):
        if self.empty():
            if self.beaten:
                return '•'
            return ['\u25A0', '\u25A1'][self.color == Color.WHITE]
        else:
            return self.figure.get_image()

    def __str__(self):
        return self.get_image()


class Board:
    board = []
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


def win_function(score):
    if score[Color.WHITE] == 0:
        return Color.BLACK
    if score[Color.BLACK] == 0:
        return Color.WHITE
    return None


def get_player_icon(color):
    if color is None:
        return '😐'
    return ['\u25CF', '\u25CB'][color == Color.WHITE]


class Checkers:
    board = Board()
    board.set_checkers()
    turn = Color.WHITE
    winner = None
    chosen_position = None

    def next_turn(self):
        self.turn = next_color(self.turn)

    def clear_mark(self):
        for line in self.board.board:
            for square in line:
                square.beaten = False

    def click_square(self, row, column):
        if self.board.board[row][column].figure is None:
            if not self.board.get_square((row, column)).beaten:
                print("Ошибка нет фигуры")
                return
            self.clear_mark()
            if self.turn == self.board.move(self.chosen_position,
                                            (row, column)):
                self.chosen_position = (row, column)
                if not self.board.can_eat(self.chosen_position):
                    self.next_turn()
                    self.chosen_position = None
                    return
                self.board.mark(self.chosen_position)
            else:
                self.chosen_position = None
                self.next_turn()
            return
        if self.board.board[row][column].figure.color != self.turn:
            print("Oшибка! Ходи своими фигурами")
            return
        if self.board.any_can_eat(self.turn) and not self.board.can_eat(
                (row, column)):
            print("Ошибка! Есть ты должен")
            return
        self.chosen_position = (row, column)

    def print(self):
        print("  0 1 2 3 4 5 6 7 8 9")
        self.board.print()

    def update(self):
        self.board.update_figures()
        self.clear_mark()
        if self.chosen_position is not None:
            self.board.mark(self.chosen_position)
        score = self.board.get_the_number_of_pieces()
        self.winner = win_function(score)

    def get_current_player_icon(self):
        return get_player_icon(self.turn)


game = Checkers()
while game.winner is None:
    try:
        game.print()
        x, y = map(int, input(
            'Выбери клетку, {}\n'.format(
                game.get_current_player_icon())).split())
        print(chr(27) + "[2J")
        game.click_square(x, y)
        game.update()
    except:
        continue
print('Победил {}'.format(get_player_icon(game.winner)))
