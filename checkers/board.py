import pygame
from .constants import SQUARE_SIZE, WHITE, BLACK, RED, ROWS, COLS
from .piece import Piece


DEFAULT_BOARD = [[WHITE,BLACK, WHITE, BLACK]]

class Board:
    def __init__(self) -> None:
        self.board = []
        self.selected_piece = None
        self.red_pieces = self.white_pieces =  12
        self.red_queens =  self.white_queens = 0

    def _draw_cubes(self, window):
        window.fill(BLACK)

        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(window, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def _fill_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row != 3 and row != 4) and col % 2  == ((row+1) % 2):
                    if row <= 2:
                        self.board[row].append(Piece(row,col,WHITE))
                    else:
                        self.board[row].append(Piece(row,col, BLACK))
                else:
                    self.board[row].append(False)

    def draw_pieces(self, window):
        self._draw_cubes(window)
        for row in range(len(self.board)):
            for piece in self.board[row]:
                if piece:
                    piece.render(window)

    def render(self, window):
        if len(self.board) == 0:
            self._fill_board()
        self.draw_pieces(window)

    def move_piece(self, piece, row, col):
        if piece:
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)
            
            if row == ROWS - 1 or row == 0:
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.red_kings += 1 

    def get_piece(self, row:int, col:int) -> Piece| bool:
        return self.board[row][col]


