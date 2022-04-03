from graphic import *


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
