
import pygame
import sys


class Tetrimino:
    def __init__(self, pieceType, board):
        self.pieceTypes = {
            "O": [[1, 1], [1, 1]],
            "L": [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
            "J": [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
            "T": [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
            "S": [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
            "Z": [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
            "I": [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
        }
        self.pieceColors = {
            "O": (255, 255, 0),
            "L": (38, 38, 229),
            "J": (255, 180, 42),
            "T": (221, 48, 221),
            "S": (48, 214, 48),
            "Z": (234, 35, 35),
            "I": (0, 210, 255)
        }

        self.srsConditions = {
            "most": {
                "01": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                "10": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                "12": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                "21": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                "23": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
                "32": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                "30": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                "03": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
            },
            "longPiece": {
                "01": [(0, 0), (-2, 0), (1, 1), (-2, -1), (1, 2)],
                "10": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
                "12": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
                "21": [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, 1)],
                "23": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
                "32": [(0, 0), (-2, 0), (1, 1), (-2, -1), (1, 2)],
                "30": [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, 1)],
                "03": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
            }
        }
        self.piece = self.pieceTypes[pieceType]
        self.color = self.pieceColors[pieceType]
        self.position = self.getSpawnPos(board)
        self.solidifying = False
        self.defaultSolidTimer = 300
        self.solidTimer = 0

    def rotatePiece(self, m):
        return [[m[j][i]
                 for j in range(len(m))] for i in range(len(m[0])-1, -1, -1)]

    def solidify(self, board):
        print("solid")
        pass

    def getSpawnPos(self, board):
        topRow = board.center[1]-board.gridSize*(board.gridDimensions[1]/2)
        if self.piece == self.pieceTypes["I"]:
            topRow -= board.gridSize
            column = board.center[0]-board.gridSize*2
        elif self.piece == self.pieceTypes["O"]:
            column = board.center[0]-board.gridSize
        else:
            column = board.center[0]-board.gridSize*2

        return (column, topRow+board.gridSize)

    def checkCollision(self, board):
        collided = False
        topRow = board.center[1]-board.gridSize*(board.gridDimensions[1]/2)
        width = board.gridSize
        offsetX = 0
        offsetY = 0
        for y in range(len(self.piece)):
            for x in range(len(self.piece[0])):
                if self.piece[y][x]:
                    if (x, y) in board.wallList or (x, y) in board.lineList:
                        if not y == topRow:
                            collided = True
                offsetX += width
            offsetX = 0
            offsetY += width
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
