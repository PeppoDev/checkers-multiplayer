import pygame
from checkers import *

# credits stackoverflow + indian guy + mind voices


def get_pos_by_mouse(pos):
    x, y = pos
    row = y // Metrics.SQUARE_SIZE.value
    col = x // Metrics.SQUARE_SIZE.value
    return row, col


FPS = 60

WINDOW = pygame.display.set_mode((Metrics.WIDTH.value, Metrics.HEIGHT.value))
pygame.display.set_caption("Checkkkers")


def main() -> None:
    run = True

    clock = pygame.time.Clock()

    game = Game(WINDOW)

    while run:
        clock.tick(FPS)

        if(game.get_winner() != None):
            print(game.get_winner())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_pos_by_mouse(pygame.mouse.get_pos())
                game.select_piece(row, col)
                game.update()

    pygame.quit()


main()
