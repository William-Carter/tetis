import pygame


class gameBoard:
    def __init__(self, gridDimensions, gridSize, center):
        self.center = center
        self.gridDimensions = gridDimensions
        self.gridSize = gridSize
        self.wallList = self.generateWalls(self.gridDimensions)
        self.lineList = []

    def generateWalls(self, gridDimensions):
        walls = []
        cursorX = 0
        cursorY = 0
        for row in range(gridDimensions[1]):
            for column in range(gridDimensions[0]):
                if row == 0 or row == gridDimensions[1]-1:
                    walls.append((cursorX, cursorY))
                else:
                    if column == 0 or column == gridDimensions[0]-1:
                        walls.append((cursorX, cursorY))

                cursorX += 1
            cursorX = 0
            cursorY += 1
        return walls

    def drawWalls(self, window, walls, pos, gridWidth):
        for wall in walls:
            pygame.draw.rect(window, (0, 0, 0),
                             pygame.Rect(wall[0]*gridWidth+pos[0], wall[1]*gridWidth+pos[1], gridWidth, gridWidth))
