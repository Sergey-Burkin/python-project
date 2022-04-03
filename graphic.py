import pygame


class Color(object):
    BLACK = 0
    WHITE = 1


FPS = 60
WIDTH, HEIGHT = 1000, 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
crown = pygame.image.load('./data/crown.png')
pygame.display.set_icon(crown)
crown.convert()
crown = pygame.transform.rotozoom(crown, 0, 0.075)
crown_rect = crown.get_rect()
BLACK_MEN_COLOR = 42, 42, 42
WHITE_MEN_COLOR = 237, 215, 197
BLACK_KING_COLOR = BLACK_MEN_COLOR
WHITE_KING_COLOR = WHITE_MEN_COLOR
BLACK_SQUARE_COLOR = 158, 90, 20
WHITE_SQUARE_COLOR = 222, 171, 100
POSSIBLE_MOVE_COLOR = 98, 120, 135


def color_to_str(color):
    if color == Color.WHITE:
        return 'White'
    if color == Color.BLACK:
        return 'Black'
