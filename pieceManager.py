import pygame
import random
import tetrimino


class PieceManager:
    def __init__(self, activePiece):
        self.activePiece = activePiece
        self.upcomingPieces = []
        #self.pieceTypes = ["I", "O", "T", "L", "J", "S", "Z"]
        self.pieceTypes = ["I"]
        self.bag = self.pieceTypes.copy()
        for i in range(6):
            self.upcomingPieces.append(self.randomPiece())
        print(self.upcomingPieces)

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
