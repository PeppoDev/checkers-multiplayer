import ast
import os
import socket
from checkers.board import Board
from checkers.constants import *
from threading import Thread
from datetime import datetime


PORT = 3337
HOST = "127.0.0.1"


class Server:
    def __init__(self) -> None:
        self.conn = self._get_connection()
        self.connections = []

    def start(self):
        print("Waiting to receive message from client")

        while True:
            conn, address = self.conn.accept()

            Thread(target=self._event_loop,
                   args=[conn, address]).start()

    def _event_loop(self,  conn, address):
        while True:
            raw_data = conn.recv(2048)

            if raw_data:
                print(raw_data.decode())
                msg = ast.literal_eval(raw_data.decode())

            else:
                break

            event = msg["event"]

            self._logger("Event received: ${0}".format(event))

            match event:
                case "join_match":
                    self._join_match(address, conn)
                case "quit_match":
                    self._quit_match()
                case "broadcast_board":
                    self.broadcast(conn, msg["data"], "update_board")

    def _get_connection(self) -> socket.socket:
        conn = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = os.getenv("SERVER_HOST") or HOST
        port = int(os.getenv("SERVER_PORT") or PORT)

        print(host, port)

        conn.bind((host, port))
        conn.listen(2)

        self._logger("listening on {0}:{1}".format(host, port))

        return conn

    def _join_match(self, address, conn):
        player = None

        if(len(self.connections) == 0):
            self.connections.append(
                {"player": Players.FIRST, "address": address, "connection": conn})
            self._logger("Player 1 {0} has entered".format(address))
            player = 'first'

        elif(len(self.connections) == 1):
            self.connections.append(
                {"player": Players.SECOND, "address": address, "connection": conn})
            self._logger("Player 2 {0} has entered".format(address))
            player = 'second'

        event = "update_player"

        self._send_message(event, player, conn)

    def _quit_match(self):
        print("Quitou")

    def broadcast(self, user_connection: socket.socket, data: any, event: str):
        for client in self.connections:
            client_conn = client["connection"]
            if client_conn != user_connection:
                self._send_message(event, data, client_conn)

    def _send_message(self, event, msg, conn):
        message = {"event": event, "data": msg,
                   "sended_at": datetime.now().isoformat()}

        conn.send(str(message).encode())

    def _logger(self, msg):
        print(msg)
