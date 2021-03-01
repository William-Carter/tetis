import pygame
import sys
import board
import tetrimino
import random
import inputController
import pieceManager
import hud
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

    testPiece = tetrimino.Tetrimino("J", board)
    pieces = ["O", "T", "L", "J", "I", "S", "Z"]
    pieceManage = pieceManager.PieceManager(testPiece)
    testPiece = tetrimino.Tetrimino(pieceManage.upcomingPieces[0], board)
    pieceManage.cyclePiece()
    pieceManage.activePiece = testPiece
    piecePreview = hud.PiecePreview(pieceManage, board)
    holdView = hud.HeldPiece(pieceManage, board)
    scoreView = hud.scoreDisplay(board)

    inputManage = inputController.InputController(testPiece)
    while going:
        frameCount += 1
        # Solidification logic
        if testPiece.solidifying:
            if testPiece.solidTimer == 0:
                testPiece.solidify(board)
                inputManage.softDropRelease()
                del testPiece
                testPiece = tetrimino.Tetrimino(
                    pieceManage.upcomingPieces[0], board)
                inputManage.tetrimino = testPiece
                inputManage.heldThisTurn = False
                pieceManage.activePiece = testPiece
                pieceManage.cyclePiece()
            else:
                testPiece.solidTimer -= 1

        # Deal with inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    inputManage.rightPress()
                if event.key == pygame.K_j:
                    inputManage.leftPress()
                if event.key == pygame.K_a:
                    testPiece.rotatePiece("L")
                if event.key == pygame.K_d:
                    testPiece.rotatePiece("R")
                if event.key == pygame.K_SPACE:
                    testPiece.hardDrop()
                if event.key == pygame.K_k:
                    inputManage.softDropPress()
                if event.key == pygame.K_LSHIFT:
                    inputManage.hold(pieceManage)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_l:
                    inputManage.rightRelease()
                if event.key == pygame.K_j:
                    inputManage.leftRelease()
                if event.key == pygame.K_k:
                    inputManage.softDropRelease()
        inputManage.onLoop()

        # Piece fall logic
        if inputManage.fallTimer % inputManage.fallSpeed == 0:
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

        board.clearFullLines(inputManage)

        # Drawing stuff
        window.fill(color)
        board.drawWalls(window, board.wallList, board.pos, board.gridSize)
        board.drawWalls(window, board.lineList, board.pos, board.gridSize)
        piecePreview.draw(window)
        holdView.draw(window)
        testPiece.draw(window, testPiece.position, gridSize, board)
        scoreView.draw(window)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()
