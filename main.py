import os, sys
import random as r
import pygame





def main():

    # GLOBAL
    GRID_WIDTH = 10
    GRID_HEIGHT = 10
    WATER_FLOW_SPEED = 5
    DIFFICULTY = None
    DEBUG = True

    #Initialize the grid
    grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    tile_selected = None
    pipe_selected = None
    # if DEBUG: print(grid)

    #Pygame
    pygame.init()
    windowW = 500
    windowH = 500
    screen = pygame.display.set_mode((windowW, windowH))
    pygame.display.set_caption("Pipe Game")
    
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                
                if pressed[pygame.K_a]:
                    rand_W = r.randint(0,GRID_WIDTH-1)
                    rand_H = r.randint(0,GRID_HEIGHT-1)
                    print(f'({rand_W},{rand_H})')
                    grid[rand_W][rand_H] = 1
            
            # Show grid in terminal
            if DEBUG:
                print("\n"*20)
                print("="*30)
                for row in grid:
                    print(row)
                print("="*30)
        


if __name__ == "__main__":
    main()