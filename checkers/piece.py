from typing import Tuple

import pygame
from .constants import BLACK, SQUARE_SIZE, GREY, CROWN

class Piece:
    PADDING = 10
    OUTLINE = 2
    def __init__(self, row: int, col: int, color: Tuple[int,int,int]) -> None:
        self.row =  row
        self.col =  col
        self.color =  color
        self.king = False

        self.calc_pos()

        if self.color == BLACK:
            self.direction = -1
        else:
            self.direction = 1


    def make_king(self):
        self.king =  True

    def render(self, window):
        radius =  SQUARE_SIZE // 2 - self.PADDING

        pygame.draw.circle(window, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        
        if self.king:
            window.blit(CROWN, (self.x -  CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def calc_pos(self):
        self.x = SQUARE_SIZE  * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE  * self.row + SQUARE_SIZE // 2
    
    def move(self, row, col):
        self.row =  row
        self.col =  col
        self.calc_pos()

    def __repr__(self) -> str:
        return str(self.color)