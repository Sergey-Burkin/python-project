from board import *


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


def color_to_pygame_color(color):
    if color == Color.WHITE:
        return WHITE_SQUARE_COLOR
    if color == Color.BLACK:
        return BLACK_SQUARE_COLOR


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

    def draw_board(self, win, position, square_width, square_height):
        for i in range(self.board.size):
            for j in range(self.board.size):
                square = self.board.get_square((i, j))
                new_position = (
                    position[0] + j * square_width,
                    position[1] + i * square_height)
                pygame.draw.rect(win, color_to_pygame_color(square.color),
                                 new_position +
                                 (square_width, square_height))

    def draw(self, win):
        square_width = WIDTH // Board.size
        square_height = HEIGHT // Board.size
        self.draw_board(win, (0, 0), square_width, square_height)
        for i in range(self.board.size):
            for j in range(self.board.size):
                square = self.board.get_square((i, j))
                square_position = j * square_width, i * square_height
                if square.figure is not None:
                    square.figure.draw(win,
                                       square_position,
                                       square_width, square_height)
                if square.beaten:
                    pygame.draw.circle(win, POSSIBLE_MOVE_COLOR,
                                       get_center_position(square_position,
                                                           square_width,
                                                           square_height),
                                       get_radius(square_width,
                                                  square_height) / 3)
        pygame.display.flip()


def start_console_game():
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


def start_gui_game():
    game = Checkers()
    clock = pygame.time.Clock()
    while game.winner is None:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x //= WIDTH // game.board.size
                y //= HEIGHT // game.board.size
                game.click_square(y, x)
        game.update()
        pygame.display.set_caption("{} move".format(color_to_str(game.turn)))
        game.draw(WIN)
        pygame.display.flip()
    pygame.display.set_caption(
        "{} is the winner!".format(color_to_str(game.winner)))
    clock.tick(1)
    clock.tick(1)
    clock.tick(1)
