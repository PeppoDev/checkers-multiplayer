import pygame
from checkers import *

def get_pos_by_mouse(pos):
    x, y = pos
    row =  y // SQUARE_SIZE
    col =  x // SQUARE_SIZE
    return row,col

FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Checkers")

def main() -> None:
    run = True

    clock = pygame.time.Clock()

    board = Board()

    board.render(WINDOW)

    piece =  board.get_piece(0,1)
    board.move_piece(piece, 4, 3)

    board.render(WINDOW)


    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_pos_by_mouse(pygame.mouse.get_pos())
                piece =  board.get_piece(row,col)
                board.move_piece(piece, 4, 3)
                board.render(WINDOW)
                pygame.display.update()

        pygame.display.update()

    pygame.quit()


main()
