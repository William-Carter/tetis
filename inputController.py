class InputController:
    def __init__(self, tetrimino):
        self.tetrimino = tetrimino
        self.regularFallSpeed = 5
        self.softDropSpeed = 1
        self.dasDelay = 10
        self.dasRepetition = 1
        self.dasTimer = 0
        self.left = 0
        self.right = 0
        self.fallTimer = 0
        self.fallSpeed = self.regularFallSpeed
        self.heldThisTurn = False
        self.direction = None

    def onLoop(self):
        self.fallTimer += 1
        if self.left == 1 and self.right == 1:
            self.direction = "right"
            self.right = 2
            self.left = 2

        elif self.left == 0 and self.right == 1:
            self.direction = "right"
            self.right = 2

        elif self.left == 1 and self.right == 0:
            self.direction = "left"
            self.left = 2

        elif self.left == 2 and self.right == 1:
            self.direction = "right"
            self.right = 2
            self.dasTimer = 0
        elif self.left == 1 and self.right == 2:
            self.direction = "left"
            self.left = 2
            self.dasTimer = 0

        if not self.left and not self.right:
            self.direction = None
            self.dasTimer = 0

        if self.direction:
            self.dasTimer += 1

        if self.dasTimer == 1:
            self.tetrimino.move(self.direction)
        if self.dasTimer >= self.dasDelay:
            if (self.dasTimer-self.dasDelay) % self.dasRepetition == 0:
                self.tetrimino.move(self.direction)

    def softDropPress(self):
        self.fallSpeed = self.softDropSpeed

    def softDropRelease(self):
        self.fallSpeed = self.regularFallSpeed

    def leftPress(self):
        if not self.tetrimino.solidTimer == 0:
            self.left = 1

    def rightPress(self):
        if not self.tetrimino.solidTimer == 0:
            self.right = 1

    def leftRelease(self):
        self.left = 0

    def rightRelease(self):
        self.right = 0

    def hold(self, pieceManager):
        if not self.heldThisTurn:
            pieceManager.holdPiece()
            self.heldThisTurn = True
