from typing import List
import pygame
from .constants import Metrics, Colors, Players
from .piece import Piece


class Board:
    def __init__(self) -> None:
        self.board = []
        self.first_player_pieces = self.second_player_pieces = 12
        self.first_player_kings = self.second_player_kings = 0

    def _draw_cubes(self, window):
        window.fill(Colors.BLACK.value)

        for row in range(Metrics.ROWS.value):
            for col in range(row % 2, Metrics.COLS.value, 2):
                pygame.draw.rect(window, Colors.GREY.value, (row * Metrics.SQUARE_SIZE.value, col *
                                 Metrics.SQUARE_SIZE.value, Metrics.SQUARE_SIZE.value, Metrics.SQUARE_SIZE.value))

    def _fill_board(self):
        for row in range(Metrics.ROWS.value):
            self.board.append([])
            for col in range(Metrics.COLS.value):
                if (row != 3 and row != 4) and col % 2 == ((row+1) % 2):
                    if row <= 2:
                        self.board[row].append(
                            Piece(row, col, Players.SECOND.value))
                    else:
                        self.board[row].append(
                            Piece(row, col, Players.FIRST.value))
                else:
                    self.board[row].append(False)

    def _draw_pieces(self, window, turn):
        self._draw_cubes(window)
        for row in range(len(self.board)):
            for col, piece in enumerate(self.board[row]):
                if piece:
                    if isinstance(piece, Piece):
                        piece.render(window, turn)
                    else:
                        new_piece = Piece(
                            piece["row"], piece["col"], piece["color"], piece["king"])
                        self.board[row][col] = new_piece

                        new_piece.render(window, turn)

    def render(self, window, turn):
        if len(self.board) == 0:
            self._fill_board()
        self._draw_pieces(window, turn)

    def move_piece(self, piece, row, col):
        if piece:
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)

            if row == Metrics.ROWS.value - 1 or row == 0:
                piece.make_king()
                if piece.color == Players.FIRST.value:
                    self.first_player_kings += 1
                else:
                    self.second_player_pieces += 1

    def get_piece(self, row: int, col: int) -> Piece | bool:
        return self.board[row][col]

    def remove(self, pieces: List[Piece]):
        for piece in pieces:
            if(piece.color == Players.FIRST.value):
                self.second_player_pieces -= 1
            else:
                self.first_player_pieces -= 1

            self.board[piece.row][piece.col] = False

    def get_valid_moves(self, piece: any):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == Players.FIRST.value or piece.king:
            moves.update(self._traverse_left(
                row - 1, max(row - 3, -1), -1, piece.color, left))

            moves.update(self._traverse_right(
                row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == Players.SECOND.value or piece.king:
            moves.update(self._traverse_left(
                row + 1, min(row+3, Metrics.ROWS.value), 1, piece.color, left))

            moves.update(self._traverse_right(
                row + 1, min(row+3, Metrics.ROWS.value), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []

        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.get_piece(r, left)

            if not current:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+r, Metrics.ROWS.value)
                    moves.update(self._traverse_left(
                        r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(
                        r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []

        for r in range(start, stop, step):
            if right >= Metrics.COLS.value:
                break

            current = self.get_piece(r, right)

            if not current:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r+3, 0)
                    else:
                        row = min(r-r, Metrics.ROWS.value)
                    moves.update(self._traverse_left(
                        r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(
                        r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1

        return moves
