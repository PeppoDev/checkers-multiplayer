import ast
import os
import socket
from datetime import datetime
from threading import Thread

import pygame
# ustom
from checkers import Game
from checkers.constants import Players


PORT = 3337
HOST = "127.0.0.1"


class Client:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.conn = self._get_connection()
        self.player = None

        self.join_match()

    def _get_connection(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = os.getenv("SERVER_HOST") or HOST
        port = int(os.getenv("SERVER_PORT") or PORT)

        conn.connect((host, port))
        Thread(target=self._event_loop, args=[conn]).start()
        return conn

    def is_my_turn(self):
        if self.player == self.game.turn:
            return True
        else:
            return False

    def select_piece(self, row, col):
        result = self.game.select_piece(row, col)
        if result:
            self._broadcast_board()

    def _broadcast_board(self):

        event = "broadcast_board"
        msg = self.game.board.board

        self._send_message(event, msg)

    def _event_loop(self, conn):
        while True:
            raw_data = conn.recv(2048)

            if raw_data:
                msg = ast.literal_eval(raw_data.decode())
            else:
                break

            event = msg["event"]

            self._logger("Event received from server: {0}".format(event))

            match event:
                case "update_player":
                    self._update_player(msg)
                case "update_turn":
                    self._update_turn(msg)
                case "update_board":
                    self._update_board(msg)
                case "error":
                    self._error_handler(msg)

    def join_match(self):
        event = "join_match"
        msg = ""

        self._send_message(event, msg)

    def quit_match(self):
        event = "quit_match"
        msg = ""

        self._send_message(event, msg)

    def update(self):
        self.game.update()

    def _update_player(self, msg):
        player = msg["data"]

        if(player == "first"):
            self.player = Players.FIRST
            pygame.display.set_caption("Checkers - Player 1")

        else:
            self.player = Players.SECOND
            pygame.display.set_caption("Checkers - Player 2")

    def _update_board(self, msg):
        board = msg["data"]
        self.game.change_turn()
        self.game.update(board)

    def _error_handler():
        pass

    def _logger(self, msg):
        print(msg)

    def _send_message(self, event, msg):
        message = {"event": event, "data": msg,
                   "sended_at": datetime.now().isoformat()}

        # self._logger(message)

        self.conn.send(str(message).encode())
