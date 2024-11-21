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
                image = pygame.transform.rotate(image, rotation)
            imageList.append(image)

    return imageList

def testLoadedImage(window, xstart, ystart, imagewidth, imageheight, imagelist, imagedict):
    """ Test function to reflect all  images """
    for row, num in enumerate(imagelist):
        for col, img in enumerate(imagedict[num]):
            window.blit(img, (xstart + (imagewidth * col), ystart + (imageheight * row)))

class Game:
    def __init__(self):
        self.sw = SCREENWIDTH
        self.sh = SCREENHEIGHT
        self.screen = pygame.display.set_mode((self.sw, self.sh))
        pygame.display.set_caption("Pipe Game")

        self.gameplay = PipeGameplay()

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

        
        """Test Load images"""
        self.testLoadImages()

        self.gameplay.draw(self.screen)

        pygame.display.update()
    
    def testLoadImages(self):
        # self.screen.blit(START["SRIGHT"][5], (500,500))
        # testLoadedImage(self.screen, 64,64,64,64,list(START.keys()), START)
        # testLoadedImage(self.screen, 64,320,64,64,list(END.keys()), END)
        # testLoadedImage(self.screen, 704,320,64,64,list(PIPES.keys()), PIPES)
        # testLoadedImage(self.screen, 64,64,64,64,list(FLOW.keys()), FLOW)
        # testLoadedImage(self.screen, 64,64,64,64,list(BOARD.keys()), BOARD)
        pass

    def debug(self):
        print("\n"*30)
        print("="*30)
        for row in grid:
            print(row)
        print("="*30)

class PipeGameplay:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLUMNS

        self.grid = self._creat_game_grid()
        self.pieces = {}

        self._insert_start_pieces(START,self._verify_start,StartPiece)
        self._insert_start_pieces(END,self._verify_end,EndPiece)
        # self._insert_end_piece()

        self.nextPieces = [r.choice(list(PIPES.keys())) for _ in range(6)]
        self.currentPiece = self.nextPieces.pop(0)


    def _creat_game_grid(self):
        """Creats an empty game grid per the numebr of rows and columns"""
        grid = []
        for row in range(self.rows):
            line = []
            for col in range(self.cols):
                line.append(" ")
            grid.append(line)
        return grid


    # removed _insert_end_piece cause they do the same thing basically
    def _insert_start_pieces(self, startpiecedict, verify_pos, newObject):
        """Randomly select a Starting Piece, then insert it into the gri in a valid position"""
        startPiece = r.choice(list(startpiecedict.keys()))
        validStartPos = False
        row,col = 0,0

        while not validStartPos:
            row, col = r.randint(0, self.rows - 1), r.randint(0, self.cols - 1)
            validStartPos = verify_pos(startPiece, self.rows, self.cols, row, col)
        
        self.pieces[(row, col)] = newObject(self, startPiece, row, col, XOFFSET, YOFFSET)
        self.grid[row][col] = self.pieces[(row, col)].piece
        return

    def _verify_start(self, startpiece, total_rows, total_cols, row, col):
        """Verify the starting location randomly selected"""
        if startpiece == "SRIGHT" and col != total_cols-1: return True
        if startpiece == "SLEFT" and col != 0: return True
        if startpiece == "SUP" and row != 0: return True
        if startpiece == "SDOWN" and row != total_rows -1: return True
        return False
    
    def _verify_end(self, endpiece, total_rows, total_cols, row, col):
        if self.grid[row][col] != " ": return False
        if row == 0 and endpiece == "EDOWN": return False
        if row == total_rows - 1 and endpiece == "EUP": return False
        if col == 0 and endpiece == "ERIGHT": return False
        if col == total_cols - 1 and endpiece == "ELEFT": return False
        else:
            if row < total_rows - 1:
                if self.grid[row + 1][col] != " ": return False
                if col < total_cols-1:
                    if self.grid[row][col+1] != " ": return False
                if col > 0:
                    if self.grid[row][col -1] != " ": return False
            elif row > 0:
                if self.grid[row-1][col] != " ": return False
        return True
    
    def draw_game_board(self, window):
        for row in range(self.rows):
            for col in range(self.cols):
                if row % 2 ==0:
                    type = "dark" if col % 2 == 0 else "light"
                else: 
                    type = "light" if col % 2 == 0 else "dark"
                window.blit(BOARD[type][0], (XOFFSET + (col * 64), YOFFSET + (row * 64)))

    def draw(self, window):
        
        self.draw_game_board(window)
        self.draw_current_next_pieces(window)
        for piece in self.pieces.values():
            piece.draw(window)     
    
    def draw_current_next_pieces(self, window):
        window.blit(pygame.transform.scale(PIPES[self.currentPiece][0], (128, 128)), (XOFFSET - 128, 64))
        pygame.draw.rect(window, "White", (XOFFSET- 128, 64, 128, 128), 1)
        for num, item, in enumerate(self.nextPieces):
            window.blit(PIPES[item][0], (XOFFSET - 96, YOFFSET + 194 + (64 * num)))
        return
        
class StartPiece:
    def __init__(self, game:Game, piece, row, col, xoffset, yoffset):
        self.game = game
        self.piece = piece
        self.row = row
        self.col = col
        self.xPos = xoffset + (self.col * CELLSIZE)
        self.yPos = yoffset + (self.row * CELLSIZE)
        self.imgIndex = 0

        self.image = START[self.piece][self.imgIndex]
        self.rect = self.image.get_rect(topleft=(self.xPos,self.yPos))
    
    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)

class EndPiece:
    def __init__(self, game, piece, row, col, xoffset, yoffset):
        self.game = game
        self.piece = piece
        self.row = row
        self.col = col
        self.xPos = xoffset + (self.col * CELLSIZE)
        self.yPos = yoffset + (self.row * CELLSIZE)
        self.end = "END"

        # using 0 instead of index because there is no animation from the end piece
        self.image = END[self.piece][0]
        self.rect = self.image.get_rect(topleft=(self.xPos,self.yPos))
    
    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)

# CONSTANTS
SCREENWIDTH = 960
SCREENHEIGHT = 896
GRID_WIDTH = 10
GRID_HEIGHT = 10
WATER_FLOW_SPEED = 5
DIFFICULTY = None
DEBUG = False
ASSETFOLDER = "assets"
ASSETPACK = "tutorial"
ROWS = 12
COLUMNS = 12
CELLSIZE = 64
XOFFSET = 128
YOFFSET = 64

IMAGESIZE = (64,64) # 64 pixels by 64

# Assets
folder = join(ASSETFOLDER,ASSETPACK)

# only one image, but rotated
START ={
    "SRIGHT": loadImages(join(folder,"pipe_start_strip11.png"),11,1,True,IMAGESIZE), # 11 image, 1 row
    "SLEFT": loadImages(join(folder,"pipe_start_strip11.png"),11,1,True,IMAGESIZE, True, 180),
    "SUP": loadImages(join(folder,"pipe_start_strip11.png"),11,1,True,IMAGESIZE, True, 90),
    "SDOWN": loadImages(join(folder,"pipe_start_strip11.png"),11,1,True,IMAGESIZE, True, -90)
}

END ={
    "ERIGHT": loadImages(join(folder,"pipe_end.png"),1,1,True,IMAGESIZE),
    "ELEFT": loadImages(join(folder,"pipe_end.png"),1,1,True,IMAGESIZE, True, 180),
    "EUP": loadImages(join(folder,"pipe_end.png"),1,1,True,IMAGESIZE, True, 90),
    "EDOWN": loadImages(join(folder,"pipe_end.png"),1,1,True,IMAGESIZE, True, -90)
}

PIPES = {
    "LR-RL": loadImages(join(folder,"pipes","pipe_horizontal.png"),1,1,True,IMAGESIZE), # just one
    "TB-BT": loadImages(join(folder,"pipes","pipe_vertical.png"),1,1,True,IMAGESIZE),
    "LT-TL": loadImages(join(folder,"pipes","pipe_corner_top_left.png"),1,1,True,IMAGESIZE),
    "LB-BL": loadImages(join(folder,"pipes","pipe_corner_bottom_left.png"),1,1,True,IMAGESIZE), # just one
    "RT-TR": loadImages(join(folder,"pipes","pipe_corner_top_right.png"),1,1,True,IMAGESIZE),
    "RB-BR": loadImages(join(folder,"pipes","pipe_corner_bottom_right.png"),1,1,True,IMAGESIZE),
}

FLOW = {
    "LR": loadImages(join(folder,"flow","water_horizontal_left_right.png"),11,1,True,IMAGESIZE),
    "Rl": loadImages(join(folder,"flow","water_horizontal_right_left.png"),11,1,True,IMAGESIZE),
    "TB": loadImages(join(folder,"flow","water_vertical_top_bottom.png"),11,1,True,IMAGESIZE),
    "BT": loadImages(join(folder,"flow","water_vertical_bottom_top.png"),11,1,True,IMAGESIZE),
    "LT": loadImages(join(folder,"flow","water_corner_left_top.png"),11,1,True,IMAGESIZE),
    "TL": loadImages(join(folder,"flow","water_corner_top_left.png"),11,1,True,IMAGESIZE),
    "LB": loadImages(join(folder,"flow","water_corner_left_bottom.png"),11,1,True,IMAGESIZE),
    "BL": loadImages(join(folder,"flow","water_corner_bottom_left.png"),11,1,True,IMAGESIZE),
    "RT": loadImages(join(folder,"flow","water_corner_right_top.png"),11,1,True,IMAGESIZE),
    "TR": loadImages(join(folder,"flow","water_corner_top_right.png"),11,1,True,IMAGESIZE),
    "RB": loadImages(join(folder,"flow","water_corner_right_bottom.png"),11,1,True,IMAGESIZE),
    "BR": loadImages(join(folder,"flow","water_corner_bottom_right.png"),11,1,True,IMAGESIZE)
}

BOARD = {
    "dark": loadImages(join(folder,"board","BoardDark.png"),1,1,True,IMAGESIZE),
    "light": loadImages(join(folder,"board","BoardLight.png"),1,1,True,IMAGESIZE)
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