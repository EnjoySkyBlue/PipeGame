import os, sys
from os.path import join
import random as r
import pygame


# Utiility funcitons

def loadSpriteSheet(path):
    """Load in a spritesheet image"""
    image = pygame.image.load(path)
    return image

def spriteImage(spritesheet, size, xcoord, ycoord, width, height):
    """Function to extract an individual image from a sprite sheet"""

    surface = pygame.surface.Surface(size)
    surface.fill("Black")
    surface.blit(spritesheet, (0,0), (xcoord, ycoord, width, height))

    surface.set_colorkey("Black") # Takes the color black on that suface and makes it transparent
    return surface

def loadImages(path, numimghor=1, numimgver=1, scaleimage=False, scalesize=(64,64), rotateimage=False, rotation=0):
    """Function to collect all sprites from a sheet into a single list"""

    spriteSheet = loadSpriteSheet(path)
    spriteSheetWidth = spriteSheet.get_width()
    spriteSheetHeight = spriteSheet.get_height()
    spriteWidth = spriteSheetWidth // numimghor
    spriteHeight = spriteSheetHeight // numimgver

    imageList = []
    for row in range(numimgver):
        for col in range(numimghor):
            image = spriteImage(spriteSheet,
                                (spriteWidth,spriteHeight),
                                col * spriteWidth, row * spriteHeight,
                                spriteWidth, spriteHeight)
            
            if scaleimage:
                image = pygame.transform.scale(image, scalesize)
            if rotateimage:
                image = pygame.transform.scale(image, rotation)
            imageList.append(image)

    return imageList
                               

class Game:
    def __init__(self):
        self.sw = SCREENWIDTH
        self.sh = SCREENHEIGHT
        self.screen = pygame.display.set_mode((self.sw, self.sh))
        pygame.display.set_caption("Pipe Game")

        self.run = True

    def runGame(self):
        while self.run:
            self.input()
            self.update()
            self.draw()

            if DEBUG:
                self.debug()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                
                # if pressed[pygame.K_a]:
                #     rand_W = r.randint(0,GRID_WIDTH-1)
                #     rand_H = r.randint(0,GRID_HEIGHT-1)
                #     print(f'({rand_W},{rand_H})')
                #     grid[rand_W][rand_H] = 1
            
    def update(self):
        pass

    def draw(self):
        self.screen.fill("Black")
        pygame.display.update()

    def debug(self):
        print("\n"*30)
        print("="*30)
        for row in grid:
            print(row)
        print("="*30)

# CONSTANTS
SCREENWIDTH = 800
SCREENHEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 10
WATER_FLOW_SPEED = 5
DIFFICULTY = None
DEBUG = True
ASSETPACK = "Default"
IMAGESIZE = (64,64) # 64 pixels by 64

# Assets
folder = join("assets",ASSETPACK)

# only one image, but rotated
START ={
    "SRIGHT": loadImages(join(folder,"pip_start_strip11.png"),11,1,True,IMAGESIZE), # 11 image, 1 row
    "SLEFT": loadImages(join(folder,"pip_start_strip11.png"),11,1,True,IMAGESIZE, True, 180),
    "SUP": loadImages(join(folder,"pip_start_strip11.png"),11,1,True,IMAGESIZE, True, 90),
    "SDOWN": loadImages(join(folder,"pip_start_strip11.png"),11,1,True,IMAGESIZE, True, -90)
}

END ={
    "ERIGHT": loadImages(join(folder,"pip_end.png"),11,1,True,IMAGESIZE), # 11 image, 1 row
    "ELEFT": loadImages(join(folder,"pip_end.png"),11,1,True,IMAGESIZE, True, 180),
    "EUP": loadImages(join(folder,"pip_end.png"),11,1,True,IMAGESIZE, True, 90),
    "EDOWN": loadImages(join(folder,"pip_end.png"),11,1,True,IMAGESIZE, True, -90)
}

PIPES = {
    
}


#Initialize the grid
grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
tile_selected = None
pipe_selected = None
# if DEBUG: print(grid)
        


if __name__ == "__main__":
    game = Game()
    game.runGame()
    pygame.quit()