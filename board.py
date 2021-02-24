import pygame


class GameBoard:
    def __init__(self, gridDimensions, gridSize, center):
        self.score = 0
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

    def scoreMetric(self, case, inpControl):
        level = 7-int(inpControl.regularFallSpeed/10)
        if level < 1:
            level = 1
        if type(case) is int:
            if case == 1:
                self.score += 100*level
            elif case == 2:
                self.score += 300*level
            elif case == 3:
                self.score += 500*level
            elif case == 4:
                self.score += 800*level

    def clearFullLines(self, inpControl):
        # Creates a dictionary of each row, and how many of its columns are filled {"row" : 8}
        lineDic = {}
        for item in self.rawLineList():
            if not str(item[1]) in lineDic:
                lineDic[str(item[1])] = 0
            lineDic[str(item[1])] += 1

        cleansedLineList = []
        deletedLines = []

        # Removes all pieces that are within any full rows
        for piece in self.lineList:
            if not lineDic[str(piece[1])] >= self.gridDimensions[0]-2:

                cleansedLineList.append(piece)
            else:
                if not piece[1] in deletedLines:
                    deletedLines.append(piece[1])

        # Counts how many lines were cleared for scoring's sake
        numberOfLinesDeleted = len(deletedLines)
        self.scoreMetric(numberOfLinesDeleted, inpControl)

        # Moves pieces down according to how many deleted rows are beneath them
        adjustedLineList = []
        for piece in cleansedLineList:
            aboveDeletedLines = 0
            for deletedLine in deletedLines:
                if piece[1] < deletedLine:
                    aboveDeletedLines += 1
            adjustedLineList.append(
                (piece[0], piece[1]+aboveDeletedLines, piece[2]))

        self.lineList = adjustedLineList.copy()
