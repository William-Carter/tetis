
import pygame
import sys


class Tetrimino:
    def __init__(self, pieceType, board):
        self.pieceTypes = {
            "O": [[1, 1], [1, 1]],
            "J": [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
            "L": [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
            "T": [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
            "S": [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
            "Z": [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
            "I": [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
        }
        self.pieceColors = {
            "O": (255, 255, 0),
            "J": (38, 38, 229),
            "L": (255, 180, 42),
            "T": (221, 48, 221),
            "S": (48, 214, 48),
            "Z": (234, 35, 35),
            "I": (0, 210, 255)
        }

        self.srsConditions = {
            "most": {
                "03": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                "30": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                "32": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                "23": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                "21": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
                "12": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                "10": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                "01": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
            },
            "longPiece": {
                "03": [(0, 0), (-2, 0), (1, 1), (-2, -1), (1, 2)],
                "30": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
                "32": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
                "23": [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, 1)],
                "21": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
                "12": [(0, 0), (-2, 0), (1, 1), (-2, -1), (1, 2)],
                "10": [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, 1)],
                "01": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
            }
        }
        self.board = board
        self.rotation = 0
        self.piece = self.pieceTypes[pieceType]
        self.pieceType = pieceType
        self.color = self.pieceColors[pieceType]
        self.position = self.getSpawnPos(self.board)
        self.solidifying = False
        self.defaultSolidTimer = 30
        self.solidTimer = 0
        self.rotString = str(self.rotation)

    def setAbsoluteRotation(self, direction):
        m = self.pieceTypes[self.pieceType]
        for i in range(direction):
            m = [[m[j][i]
                  for j in range(len(m))] for i in range(len(m[0])-1, -1, -1)]
        self.piece = m

    def rotatePiece(self, direction):
        if self.solidTimer == 0:
            return 0
        originalPos = self.position
        originalRotation = self.rotation
        rotations = {"0": [3, 1], "1": [0, 2], "2": [1, 3], "3": [2, 0]}
        targetRotation = rotations[str(self.rotation)]
        validPosFound = False
        if direction == "R":
            targetRotation = targetRotation[0]
        else:
            targetRotation = targetRotation[1]
        self.setAbsoluteRotation(targetRotation)
        self.rotation = targetRotation

        if self.pieceType == "I":
            srsConditionToBeUsed = "longPiece"
        else:
            srsConditionToBeUsed = "most"

        for offset in self.srsConditions[srsConditionToBeUsed][str(originalRotation)+str(targetRotation)]:
            self.position = (
                self.position[0]+offset[0]*self.board.gridSize, self.position[1]+(offset[1]*-1)*self.board.gridSize)
            if not self.checkCollision(self.board):
                validPosFound = True
                break
            else:
                self.position = originalPos
                self.rotation = originalRotation
        if not validPosFound:
            self.rotation = originalRotation
            self.position = originalPos
            self.setAbsoluteRotation(originalRotation)
        else:
            self.rotation = targetRotation

    def solidify(self, board):
        width = 1
        offsetX = 0
        offsetY = 0
        for y in range(len(self.piece)):
            for x in range(len(self.piece[0])):
                if self.piece[y][x]:
                    board.lineList.append((self.position[0]/board.gridSize+offsetX-board.pos[0]/board.gridSize,
                                           self.position[1]/board.gridSize+offsetY-board.pos[1]/board.gridSize, self.color))
                offsetX += width
            offsetX = 0
            offsetY += width

    def getSpawnPos(self, board):
        topRow = board.center[1]-board.gridSize*(board.gridDimensions[1]//2)
        if self.piece == self.pieceTypes["I"]:
            topRow -= board.gridSize
            column = board.center[0]-board.gridSize*2
        elif self.piece == self.pieceTypes["O"]:
            column = board.center[0]-board.gridSize
        else:
            column = board.center[0]-board.gridSize*2

        return (column, topRow+board.gridSize)

    def move(self, direction):
        dir = 1
        if direction == "left":
            dir = -1
        self.position = (self.position[0] +
                         self.board.gridSize*dir, self.position[1])
        if self.checkCollision(self.board):
            self.position = (self.position[0] -
                             self.board.gridSize*dir, self.position[1])

    def fixPos(self):
        self.position = (
            int(self.position[0]), int(self.position[1]))

    def checkCollision(self, board):
        collided = False
        topRow = board.center[1]-board.gridSize*(board.gridDimensions[1]/2)
        offsetX = 0
        offsetY = 0

        # Iterate through each item in the piece list (like [0, 0, 0] or whatever)
        for y in range(len(self.piece)):
            for x in range(len(self.piece[0])):
                # Checks if the item is 1 (if it isn't it's just empty space)
                if self.piece[y][x]:
                    # Forgive me lord for I have sinned (check if it's in the wall or in the existing pieces)
                    if (self.position[0]/board.gridSize+offsetX-board.pos[0]/board.gridSize, self.position[1]/board.gridSize+offsetY-board.pos[1]/board.gridSize) in board.wallList or (self.position[0]/board.gridSize+offsetX-board.pos[0]/board.gridSize, self.position[1]/board.gridSize+offsetY-board.pos[1]/board.gridSize) in board.rawLineList():
                        # Don't deal with collision with the top row of the board
                        if not self.position[1]/board.gridSize+offsetY-board.pos[1]/board.gridSize == topRow:
                            collided = True
                offsetX += 1
            offsetX = 0
            offsetY += 1

        return collided

    def draw(self, window, pos, width, board):
        offsetX = 0
        offsetY = 0
        for y in range(len(self.piece)):
            for x in range(len(self.piece[0])):
                if self.piece[y][x]:
                    if not y >= (board.center[1]-board.gridSize*(board.gridDimensions[1]/2)):
                        pygame.draw.rect(window, self.color,
                                         pygame.Rect(pos[0]+offsetX, pos[1]+offsetY, width, width))
                offsetX += width
            offsetX = 0
            offsetY += width

        # Draw the center dot
        pygame.draw.rect(window, (0, 0, 0),
                         pygame.Rect(pos[0]+len(self.piece)*width/2, pos[1]+len(self.piece)*width/2, 2, 2))

    def hardDrop(self):
        stuck = False

        while not stuck:
            self.backupPos = self.position
            self.position = (self.position[0],
                             self.position[1]+self.board.gridSize)
            if self.checkCollision(self.board):
                stuck = True
                self.position = self.backupPos
                self.solidTimer = 0
