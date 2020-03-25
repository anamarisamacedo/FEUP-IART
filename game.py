from pygame.sprite import groupcollide
from AI import *
from bubble import *

rowNr = 6
colNr = 5
windowWidth = 100*colNr
windowHeight = 100*rowNr
scoreVerticalSpace = 80

center = (windowWidth/2, windowHeight/2)

class Game():
    def __init__(self, startGrid, touches):
        self.win = pygame.display.set_mode((windowWidth, windowHeight + scoreVerticalSpace))
        self.startGrid = startGrid
        self.bubbles = pygame.sprite.Group()
        self.score = 0
        self.touchesLeft = touches
        self.projectiles = pygame.sprite.Group()

        pygame.init()
        pygame.display.set_caption("Bubble blast")
        self.createBubbles()


    def createBubbles(self):
        # create bubble list
        for i in range(0, len(self.startGrid[0])):
            for j in range(0, len(self.startGrid)):
                # dont create level 0 balls
                if self.startGrid[j][i] > 0:
                    self.bubbles.add(Bubble((100 * i + 50, 100 * j + scoreVerticalSpace), self.startGrid[j][i]))


    # animate a move
    def makeMove(self, bubble):
        # if bubble is clicked, make it get hit and decrement touchesLeft
        newExplosion = bubble.hit()

        # if bubble dies, add explosions
        if newExplosion != None:
            self.score += bubble.score
            self.bubbles.remove(bubble)

            self.projectiles.add(newExplosion[0][0])
            self.projectiles.add(newExplosion[0][1])
            self.projectiles.add(newExplosion[0][2])
            self.projectiles.add(newExplosion[0][3])

    def playHuman(self):

        gameOver = False
        while (not gameOver):

            self.update()

            # avoid clicking before move ends
            if len(self.projectiles) <= 0 and self.touchesLeft > 0:
                # check mouse events

                for event in pygame.event.get():
                    # check mouse click on exit button
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    # check mouse click on bubble
                    if event.type == pygame.MOUSEBUTTONUP:
                        for bubble in self.bubbles:
                            if bubble.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                                self.makeMove(bubble)
                                self.touchesLeft -= 1
                                break

            if len(self.projectiles) <= 0:
                if len(self.bubbles) <= 0:
                    self.writeToScreen(center, "You won!", True)
                    gameOver = True

                elif self.touchesLeft <= 0:
                    self.writeToScreen(center, "Game over :(", True)
                    gameOver = True

            # update whole screen
            pygame.display.flip()

            # fill background
            self.win.fill((0, 0, 0))

    def playComputer(self):
        gameOver = False

        moves = []
        waitingForSelection = True
        ai = AI(self.startGrid, self.touchesLeft)

        #Select AI mode
        while waitingForSelection:
            self.writeToScreen(center, "Press A to BFS algorithm", True)
            self.writeToScreen((center[0], center[1] + 40), "Press B to DFS algorithm", False)
            self.writeToScreen((center[0], center[1] + 80), "Press C to IDDFS algorithm", False)
            self.writeToScreen((center[0], center[1] + 120), "Press D to Greedy algorithm", False)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        moves = ai.BFS()
                        waitingForSelection = False

                    if event.key == pygame.K_b:
                        moves = ai.dfs()
                        waitingForSelection = False

                    if event.key == pygame.K_c:
                        moves = ai.iddfs_algorithm()
                        waitingForSelection = False

                    if event.key == pygame.K_d:
                        moves = ai.greedy_algorithm()
                        waitingForSelection = False

        waitBetweenMoves = False
        self.update()
        pygame.display.flip()
        pygame.time.wait(1000)

        while (not gameOver):
            self.update()
            pygame.display.flip()

            if waitBetweenMoves:
                pygame.time.wait(1000)
                waitBetweenMoves = False

            #if previous move ended, and there are more moves to play, play next move
            if len(self.projectiles) == 0 and len(moves) > 0:
                move = moves.pop(0)
                for bubble in self.bubbles:
                    if bubble.rect.collidepoint(100 * move[1] + 50, 100 * move[0] + scoreVerticalSpace):

                        if bubble.level > 1:
                            waitBetweenMoves = True

                        self.makeMove(bubble)
                        self.touchesLeft -= 1
                        break

            if len(self.projectiles) <= 0:
                if len(self.bubbles) <= 0:
                    self.writeToScreen(center, "You won!", True)
                    gameOver = True

                elif self.touchesLeft <= 0 or len(moves) == 0:
                    self.writeToScreen(center, "Game over :(", True)
                    gameOver = True

            # update whole screen
            pygame.display.flip()

            # fill background
            self.win.fill((0, 0, 0))

    # write text in the screen
    def writeToScreen(self, pos, text, clearScreen):
        if clearScreen:
            self.win.fill((0, 0, 0))

        smallfont = pygame.font.SysFont("Arial", 25)
        textSurf = smallfont.render(text, True, (255, 255, 255))
        textRect = textSurf.get_rect()
        textRect.center = pos
        self.win.blit(textSurf, textRect)

    # checks collision between sprites, removes projectiles which hit balls
    def checkCollisions(self):
        # dictionary with bubbles and projectiles which collided
        ballsHit = groupcollide(self.bubbles, self.projectiles, False, True)
        scoreAddition = 0

        for bubble in ballsHit.keys():

            # fix case when bubble is hit multiple times simultaneously
            for hit in range(0, len(ballsHit[bubble]) - 1):
                bubble.hit()

            newExplosion = bubble.hit()

            if newExplosion != None:
                scoreAddition += bubble.score * len(ballsHit[bubble])
                self.bubbles.remove(bubble)
                self.projectiles.add(newExplosion[0][0])
                self.projectiles.add(newExplosion[0][1])
                self.projectiles.add(newExplosion[0][2])
                self.projectiles.add(newExplosion[0][3])

        # remove projectiles that leave screen
        for projectile in self.projectiles:
            if projectile.x < 0 or projectile.y < 0 or projectile.x > windowWidth or projectile.y > windowHeight:
                self.projectiles.remove(projectile)

        return scoreAddition

    def update(self):
        # update bubbles, projectiles
        self.bubbles.update()
        self.projectiles.update()

        # check collisions between projectiles and bubbles. update score
        self.score += self.checkCollisions()

        # draw all entities
        self.writeToScreen((center[0], 20), "Score: " + str(self.score), True)
        self.writeToScreen((center[0], windowHeight + 50), "Touches left: " + str(self.touchesLeft), False)
        self.bubbles.draw(self.win)
        self.projectiles.draw(self.win)

