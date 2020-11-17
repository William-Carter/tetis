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
    pieceManage.activePiece = testPiece
    piecePreview = hud.PiecePreview(pieceManage, board)

    inputManage = inputController.InputController(testPiece)
    while going:
        frameCount += 1
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    inputManage.rightPress()
                elif event.key == pygame.K_j:
                    inputManage.leftPress()
                if event.key == pygame.K_a:
                    testPiece.rotatePiece("L")
                elif event.key == pygame.K_d:
                    testPiece.rotatePiece("R")
                if event.key == pygame.K_SPACE:
                    testPiece.hardDrop()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_l:
                    inputManage.rightRelease()
                elif event.key == pygame.K_j:
                    inputManage.leftRelease()

        inputManage.onLoop()

        # Piece fall logic
        if frameCount % 4 == 0:
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
                testPiece = tetrimino.Tetrimino(
                    pieceManage.upcomingPieces[0], board)
                inputManage.tetrimino = testPiece
                pieceManage.cyclePiece()
            else:
                testPiece.solidTimer -= 1
        board.clearFullLines()

        # Drawing stuff
        window.fill(color)
        testPiece.draw(window, testPiece.position, gridSize, board)
        board.drawWalls(window, board.wallList, board.pos, board.gridSize)
        board.drawWalls(window, board.lineList, board.pos, board.gridSize)
        piecePreview.draw(window)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()
