import pygame


class PieceDisplay:
    def __init__(self, board):
        self.board = board

    def drawTetrimino(self, window, pieceArray, pieceType, pos, color):
        offsetX = 0
        offsetY = 0
        piece = pieceArray[pieceType]
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x]:
                    pygame.draw.rect(window, color,
                                     pygame.Rect(pos[0]+offsetX, pos[1]+offsetY, self.board.gridSize, self.board.gridSize))
                offsetX += self.board.gridSize
            offsetX = 0
            offsetY += self.board.gridSize


class PiecePreview(PieceDisplay):
    def __init__(self, pieceManager, board):
        super().__init__(board)
        self.pieceManager = pieceManager
        boardTop = board.center[1]-(board.gridDimensions[1]/2)*board.gridSize
        self.position = (board.center[0] +
                         board.gridSize*(board.gridDimensions[0]/2+2), boardTop)

    def draw(self, window):
        level = 0
        for item in self.pieceManager.upcomingPieces:

            color = self.pieceManager.activePiece.pieceColors[item]
            if not level/4 > 6:
                self.drawTetrimino(window,  self.pieceManager.activePiece.pieceTypes,
                                   item, (self.position[0], self.position[1]+level*self.board.gridSize), color)
            level += 4


class HeldPiece(PieceDisplay):
    def __init__(self, pieceManager, board):
        super().__init__(board)
        self.pieceManager = pieceManager
        boardTop = board.center[1]-(board.gridDimensions[1]/2)*board.gridSize
        self.position = (board.center[0] -
                         board.gridSize*(board.gridDimensions[0]/2+4), boardTop)

    def draw(self, window):
        if self.pieceManager.heldPiece:
            self.drawTetrimino(window, self.pieceManager.activePiece.pieceTypes, self.pieceManager.heldPiece, self.position,
                               self.pieceManager.activePiece.pieceColors[self.pieceManager.heldPiece])


class GhostPiece(PieceDisplay):
    def __init__(self, activePiece, board):
        super().__init__()
