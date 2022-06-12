from pygame import Surface
import pygame

from checkers.board import Board
from checkers.constants import Metrics, Mode, Players, Colors


class Game:
    def __init__(self, window: Surface) -> None:
        self.window = window
        self._ignite()
        self.update()

    def _ignite(self):
        self.board = Board()
        self.turn = Players.FIRST
        self.valid_moves = {}
        self.selected = None
        self.mode = Mode.ONLINE

    def update(self, board=None):
        if board:
            self.board.board = board

        self.board.render(self.window, self.turn.value)
        self._draw_valid_moves(self.valid_moves)

    def reset(self):
        self._ignite()

    def select_piece(self, row, col):
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select_piece(row, col)
            else:
                return True

        piece = self.board.get_piece(row, col)

        if piece and piece.color == self.turn.value:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)

        return False

    def move(self, row, col):
        piece_target = self.board.get_piece(row, col)
        if self.selected and not piece_target and (row, col) in self.valid_moves:
            self.board.move_piece(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]

            if skipped:
                self.board.remove(skipped)

            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):

        self.valid_moves = {}
        if self.turn == Players.FIRST:
            self.turn = Players.SECOND
        else:
            self.turn = Players.FIRST

    def get_winner(self):
        if self.board.first_player_pieces == 0:
            return Players.SECOND.value
        elif self.board.second_player_pieces == 0:
            return Players.FIRST.value
        else:
            return None

    def _draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, Colors.GREEN.value, (col * Metrics.SQUARE_SIZE.value +
                               Metrics.SQUARE_SIZE.value//2, row * Metrics.SQUARE_SIZE.value + Metrics.SQUARE_SIZE.value//2), 15)
