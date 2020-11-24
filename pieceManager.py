import random
import pygame
import tetrimino


class PieceManager:
    def __init__(self, activePiece):
        self.activePiece = activePiece
        self.upcomingPieces = []
        self.pieceTypes = ["I", "O", "T", "L", "J", "S", "Z"]
        self.bag = self.pieceTypes.copy()
        self.heldPiece = ""
        for i in range(6):
            self.upcomingPieces.append(self.randomPiece())

    def cyclePiece(self):
        self.upcomingPieces.pop(0)
        self.upcomingPieces.append(self.randomPiece())

    def randomPiece(self):
        if len(self.bag) == 1:
            last = self.bag[0]
            self.bag = self.pieceTypes.copy()

            return last
        piece = random.choice(self.bag)
        self.bag.remove(piece)
        return piece

    def holdPiece(self):
        board = self.activePiece.board
        if self.heldPiece:
            tempPiece = self.activePiece.pieceType
            self.activePiece.__init__(self.heldPiece, board)
            self.heldPiece = tempPiece
        else:
            self.heldPiece = self.activePiece.pieceType
            self.activePiece.__init__(
                self.upcomingPieces[0], board)
            self.cyclePiece()
