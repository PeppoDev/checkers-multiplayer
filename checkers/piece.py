from typing import Tuple

import pygame
from .constants import Metrics, Colors, Assets


class Piece:
    PADDING = 10
    OUTLINE = 4

    def __init__(self, row: int, col: int, color: Tuple[int, int, int]) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.calc_pos()

    def make_king(self):
        self.king = True

    def render(self, window, turn: any):
        radius = Metrics.SQUARE_SIZE.value // 2 - self.PADDING

        border_color = Colors.GREEN.value if turn == self.color else Colors.GREY.value

        pygame.draw.circle(window, border_color,
                           (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)

        if self.king:
            window.blit(Assets.CROWN.value, (self.x - Assets.CROWN.value.get_width() //
                        2, self.y - Assets.CROWN.value.get_height()//2))

    def calc_pos(self):
        self.x = Metrics.SQUARE_SIZE.value * self.col + Metrics.SQUARE_SIZE.value // 2
        self.y = Metrics.SQUARE_SIZE.value * self.row + Metrics.SQUARE_SIZE.value // 2

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self) -> str:
        return str(self.color)
