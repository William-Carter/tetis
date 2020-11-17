import pygame


class GameBoard:
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

    def rawLineList(self):
        raw = []
        for item in self.lineList:
            raw.append((item[0], item[1]))

        return raw

    def drawWalls(self, window, walls, pos, gridWidth):

        for wall in walls:
            if len(wall) > 2:
                color = wall[2]
            else:
                color = (0, 0, 0)
            pygame.draw.rect(window, color,
                             pygame.Rect(wall[0]*gridWidth+pos[0], wall[1]*gridWidth+pos[1], gridWidth, gridWidth))

    def clearFullLines(self):
        lineDic = {}
        for item in self.rawLineList():
            if not str(item[1]) in lineDic:
                lineDic[str(item[1])] = 0
            lineDic[str(item[1])] += 1

        self.lineList = list(dict.fromkeys(self.lineList))
        clearedLines = []
        delWidth = self.gridDimensions[0]-2
        for yCor in lineDic:
            if lineDic[yCor] >= delWidth:
                clearedLines.append(yCor)
                newLineList = []
                for item in self.lineList:
                    if not str(item[1]) == yCor:
                        newLineList.append(item)
                newNewLineList = []
                for item in newLineList:
                    moveDown = 0
                    for line in clearedLines:
                        if item[1] < float(line):
                            moveDown += 1
                    newNewLineList.append((item[0], item[1]+moveDown, item[2]))

                self.lineList = newNewLineList.copy()
