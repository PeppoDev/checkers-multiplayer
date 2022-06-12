from connection import Server
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    server = Server()
    server.start()
