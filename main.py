import pygame
import sys
import board
import tetrimino
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
    board = board.gameBoard(boardDimesions, gridSize, (midWidth, midHeight))

    testPiece = tetrimino.Tetrimino("T", board)
    pieces = ["O", "T", "L", "J", "I", "S", "Z"]
    while going:
        frameCount += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False

        if frameCount % 60 == 0:
            testPiece.position = (
                testPiece.position[0], testPiece.position[1] + gridSize)
            if testPiece.checkCollision(board):
                testPiece.position = (
                    testPiece.position[0], testPiece.position[1] - gridSize)
                testPiece.solidifying = True
            else:
                testPiece.solidifying = False
                testPiece.solidTimer = testPiece.defaultSolidTimer
        if testPiece.solidifying:
            if testPiece.solidTimer == 0:
                testPiece.solidify(board)
            else:
                testPiece.solidTimer -= 1

        window.fill(color)
        testPiece.draw(window, testPiece.position, gridSize, board)
        board.drawWalls(window, board.wallList, (midWidth-board.gridSize *
                                                 board.gridDimensions[0]/2, midHeight-board.gridSize *
                                                 board.gridDimensions[1]/2), board.gridSize)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()
