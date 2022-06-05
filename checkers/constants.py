
import pygame

# metrics
WIDTH, HEIGHT =  800, 800
ROWS, COLS =  8,8
SQUARE_SIZE = WIDTH//COLS

## colors

# RGB
RED = (255, 0 ,0)
BLUE = (0, 0, 255)
GREEN =  (0, 255, 0)

# neutrals
BLACK =  (0,0,0)
WHITE =  (255, 255, 255)
GREY = (105,105,105)

# assets
CROWN =  pygame.transform.scale(pygame.image.load("assets/crown.png"), (44,25))
