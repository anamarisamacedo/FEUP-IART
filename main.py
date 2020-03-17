from pygame.sprite import groupcollide

from bubble import *

import time

# level bubbles
bubbles = pygame.sprite.Group()

# explosions when bubble dies
projectiles = pygame.sprite.Group()


windowWidth = 400
windowHeight = 600
scoreVerticalSpace = 80
win = pygame.display.set_mode((windowWidth, windowHeight + scoreVerticalSpace))


def writeToScreen(pos, text, clearScreen):
    if clearScreen:
        win.fill((0, 0, 0))

    smallfont = pygame.font.SysFont("Arial", 25)
    textSurf = smallfont.render(text, True, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.center = pos
    win.blit(textSurf, textRect)


def checkCollisions():
    # dictionary with bubbles and projectiles which collided
    # this function also removes all colliding projectiles from the list
    ballsHit = groupcollide(bubbles, projectiles, False, True)
    scoreAddition = 0

    for bubble in ballsHit.items():
        newExplosion = bubble[0].hit()

        if newExplosion != None:
            scoreAddition += bubble[0].score
            bubbles.remove(bubble[0])
            projectiles.add(newExplosion[0][0])
            projectiles.add(newExplosion[0][1])
            projectiles.add(newExplosion[0][2])
            projectiles.add(newExplosion[0][3])

    return scoreAddition


# Project main loop
def game(startGrid, touchesLeft):
    pygame.init()
    pygame.display.set_caption("Bubble blast")

    score = 0
    gameOver = False

    # create bubble list
    for i in range(0, len(startGrid[0])):
        for j in range(0, len(startGrid)):
            bubbles.add(Bubble((100 * i + 50, 100 * j + scoreVerticalSpace), startGrid[j][i]))

    intro = run = True
    while run:

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False

            writeToScreen(((len(startGrid[0]) * 100 / 2), (len(startGrid) * 100 / 2)), "Press C to play human mode.", True)

            pygame.display.flip()

        while(not gameOver):

            # update bubbles, projectiles
            bubbles.update()
            projectiles.update()

            # check collisions between projectiles and bubbles. update score
            score += checkCollisions()

            # draw all entities
            writeToScreen((windowWidth / 2, 20), "Score: " + str(score), False)

            writeToScreen((windowWidth / 2, windowHeight + 50), "Touches left: " + str(touchesLeft), False)

            bubbles.draw(win)
            projectiles.draw(win)

            # check mouse events
            for event in pygame.event.get():

                # check mouse click on exit button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # check mouse click on bubble
                if event.type == pygame.MOUSEBUTTONUP:
                    for bubble in bubbles:
                        if bubble.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            # if bubble is clicked, make it get hit and decrement touchesLeft
                            newExplosion = bubble.hit()
                            touchesLeft -= 1

                            if touchesLeft < 0:
                                writeToScreen((windowWidth/2, windowHeight/2), "Game over :(", True)
                                gameOver = True
                                break

                            # if bubble dies, add explosions
                            if newExplosion != None:
                                score += bubble.score
                                bubbles.remove(bubble)

                                projectiles.add(newExplosion[0][0])
                                projectiles.add(newExplosion[0][1])
                                projectiles.add(newExplosion[0][2])
                                projectiles.add(newExplosion[0][3])


            if len(bubbles) == 0:
                writeToScreen((windowWidth/2, windowHeight/2), "You won! :D", True)
                gameOver = True


            # update whole screen
            pygame.display.flip()

            # fill background
            win.fill((0, 0, 0))


        # check mouse events
        for event in pygame.event.get():

            # check mouse click on exit button
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



touchesLeft = 3
startGrid = []
startGrid.append([1, 2, 2, 1])
startGrid.append([1, 2, 1, 1])
startGrid.append([1, 2, 4, 1])
startGrid.append([2, 1, 1, 2])
startGrid.append([3, 4, 3, 3])
startGrid.append([2, 1, 2, 1])

game(startGrid, touchesLeft)
