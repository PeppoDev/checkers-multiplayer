import pygame
from checkers import *
from connection import Client
from dotenv import load_dotenv


def get_pos_by_mouse(pos):
    x, y = pos
    row = y // Metrics.SQUARE_SIZE.value
    col = x // Metrics.SQUARE_SIZE.value
    return row, col


FPS = 60

WINDOW = pygame.display.set_mode((Metrics.WIDTH.value, Metrics.HEIGHT.value))
pygame.display.set_caption("Checkers")

load_dotenv()


def main() -> None:

    run = True

    clock = pygame.time.Clock()

    game = Game(WINDOW)

    client = Client(game)

    while run:
        clock.tick(FPS)

        if(game.get_winner() != None):
            print(game.get_winner())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.quit_match()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if(client.is_my_turn()):
                    row, col = get_pos_by_mouse(pygame.mouse.get_pos())
                    client.select_piece(row, col)
                    client.update()

        pygame.display.update()

    pygame.quit()


main()
