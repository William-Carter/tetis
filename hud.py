import pygame


class PieceDisplay:
    def __init__(self, pieceManager, board):
        self.pieceManager = pieceManager
        self.board = board

    def drawTetrimino(self, window, pieceType, pos, color):
        offsetX = 0
        offsetY = 0
        piece = self.pieceManager.activePiece.pieceTypes[pieceType]
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
        super(PiecePreview, self).__init__(pieceManager, board)
        boardTop = board.center[1]-(board.gridDimensions[1]/2)*board.gridSize
        self.position = (board.center[0] +
                         board.gridSize*(board.gridDimensions[0]/2+2), boardTop)

    def draw(self, window):
        level = 0
        for item in self.pieceManager.upcomingPieces:
            color = self.pieceManager.activePiece.pieceColors[item]
            self.drawTetrimino(window,
                               item, (self.position[0], self.position[1]+level*self.board.gridSize), color)
            level += 4


class HeldPiece(PieceDisplay):
    def __init__(self, pieceManager, board):
        super(PiecePreview, self).__init__(pieceManager, board)
        boardTop = board.center[1]-(board.gridDimensions[1]/2)*board.gridSize
