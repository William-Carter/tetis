import pygame
import sys
import board
import tetrimino
import random
import inputController
windowHeight = 720
windowWidth = 1080
midHeight = windowHeight/2
midWidth = windowWidth/2
pygame.init()
window = pygame.display.set_mode(
    (windowWidth, windowHeight), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Tetis")
clock = pygame.time.Clock()

if __name__ == "__main__":
    frameCount = 0
    going = True
    color = (255, 255, 255)
    boardDimesions = (12, 22)
    gridSize = 30
    board = board.GameBoard(boardDimesions, gridSize, (midWidth, midHeight))
    board.pos = (midWidth-board.gridSize *
                 board.gridDimensions[0]/2, midHeight-board.gridSize *
                 board.gridDimensions[1]/2)

    testPiece = tetrimino.Tetrimino("T", board)
    pieces = ["O", "T", "L", "J", "I", "S", "Z"]

    inputManage = inputController.InputController(testPiece)
    while going:
        frameCount += 1
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    inputManage.rightPress()
                elif event.key == pygame.K_a:
                    inputManage.leftPress()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    inputManage.rightRelease()
                elif event.key == pygame.K_a:
                    inputManage.leftRelease()

        inputManage.onLoop()

        # Piece fall logic
        if frameCount % 20 == 0:
            testPiece.position = (
                testPiece.position[0], testPiece.position[1] + gridSize)
            testPiece.fixPos()
            if testPiece.checkCollision(board):
                testPiece.position = (
                    testPiece.position[0], testPiece.position[1] - gridSize)
                testPiece.fixPos()
                testPiece.solidifying = True
            else:
                testPiece.solidifying = False
                testPiece.solidTimer = testPiece.defaultSolidTimer

        # Solidifiaction logic
        if testPiece.solidifying:
            if testPiece.solidTimer == 0:
                testPiece.solidify(board)
                testPiece = tetrimino.Tetrimino(random.choice(pieces), board)
                inputManage.tetrimino = testPiece
            else:
                testPiece.solidTimer -= 1

        # Drawing stuff
        window.fill(color)
        testPiece.draw(window, testPiece.position, gridSize, board)
        board.drawWalls(window, board.wallList, board.pos, board.gridSize)
        board.drawWalls(window, board.lineList, board.pos, board.gridSize)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()
