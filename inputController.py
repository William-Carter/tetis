class InputController:
    def __init__(self, tetrimino):
        self.tetrimino = tetrimino
        self.dasDelay = 10
        self.dasRepetition = 1
        self.leftTimer = 0
        self.rightTimer = 0
        self.left = False
        self.right = False

    def onLoop(self):
        if self.leftTimer == 1:
            self.tetrimino.move("left")
        if self.leftTimer >= self.dasDelay:
            if (self.leftTimer-self.dasDelay) % self.dasRepetition == 0:
                self.tetrimino.move("left")

        if self.rightTimer == 1:
            self.tetrimino.move("right")

        if self.rightTimer >= self.dasDelay:
            if (self.rightTimer-self.dasDelay) % self.dasRepetition == 0:
                self.tetrimino.move("right")

        if self.left:
            self.leftTimer += 1

        if self.right:
            self.rightTimer += 1

    def leftPress(self):
        if not self.tetrimino.solidTimer == 0:
            self.leftTimer = 1
            self.left = True
            self.rightRelease()

    def rightPress(self):
        if not self.tetrimino.solidTimer == 0:
            self.rightTimer = 1
            self.right = True
            self.leftRelease()

    def leftRelease(self):
        self.leftTimer = 0
        self.left = False

    def rightRelease(self):
        self.rightTimer = 0
        self.right = False
