from pygame.sprite import groupcollide
from AI import *
from bubble import *

windowWidth = 100*colNr
windowHeight = 100*rowNr
center = (windowWidth/2, windowHeight/2)

class Game():
    def __init__(self, levels):
        self.win = pygame.display.set_mode((windowWidth, windowHeight + scoreVerticalSpace))
        self.bubbles = pygame.sprite.Group()
        self.score = 0
        self.projectiles = pygame.sprite.Group()
        self.levels = levels

        pygame.init()
        pygame.display.set_caption("Bubble blast")

    def setLevel(self, level):
        self.startGrid = self.levels[level-1][1]
        self.touchesLeft = self.levels[level-1][2]
        self.solution = self.levels[level-1][3]

        self.createBubbles()

    #create list of bubbles
    def createBubbles(self):
        # create bubble list
        for i in range(0, len(self.startGrid[0])):
            for j in range(0, len(self.startGrid)):
                # dont create level 0 balls
                if self.startGrid[j][i] > 0:
                    self.bubbles.add(Bubble((i, j), self.startGrid[j][i]))

    #Recieves list of key presses to check for
    def checkInputs(self, options):
        # check mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN:
                if event.key in options:
                    return event.key

    def checkReturnToMenu(self):
        while True:
            self.writeToScreen((center[0], center[1] + 40), "Y - Go back to main menu", False)
            self.writeToScreen((center[0], center[1] + 80), "Q - Quit game", False)
            pygame.display.flip()

            input = self.checkInputs([pygame.K_y, pygame.K_q])
            if input == pygame.K_y : return True
            elif input == pygame.K_q:
                pygame.quit()
                quit()

    #decrements clicked bubble's level, creates projectiles if the bubble explodes (if it's a level 1 bubble)
    def makeMove(self, bubble):
        self.ai.grid = self.ai.clickBubble(self.ai.grid, (bubble.pos[1], bubble.pos[0]))
        self.ai.touchesLeft -= 1
        # if bubble is clicked, make it get hit and decrement touchesLeft
        newExplosion = bubble.hit()

        # if bubble explodes (level 1), add explosions
        if newExplosion != None:
            self.score += bubble.score
            self.bubbles.remove(bubble)

            self.projectiles.add(newExplosion[0][0])
            self.projectiles.add(newExplosion[0][1])
            self.projectiles.add(newExplosion[0][2])
            self.projectiles.add(newExplosion[0][3])

    #logic for human mode
    def playHuman(self):
        gameOver = False
        hint = False
        self.ai = AI(self.startGrid, self.touchesLeft)
        while (not gameOver):

            self.update()

            # avoid clicking before move ends
            if len(self.projectiles) <= 0 and self.touchesLeft > 0:

                # check mouse/kbd events
                input = self.checkInputs([pygame.K_h])

                if input == pygame.K_h:
                    self.win.fill((0, 0, 0))
                    pygame.display.flip()
                    moves = self.ai.iddfs_algorithm()
                    pos = 0
                    if type(moves) == None:
                        self.writeToScreen(center, "No solution exists for the current state :(", False)
                        pygame.display.flip()
                    else:
                        for move in moves:
                            self.writeToScreen((center[0], center[1] + pos), str(move), False)
                            pygame.display.flip()
                            pos += 40

                    pygame.time.wait(5000)

                elif input != None:
                    for bubble in self.bubbles:
                        #if a bubble was clicked
                        if bubble.rect.collidepoint(input[0], input[1]):
                            self.makeMove(bubble)
                            self.touchesLeft -= 1
                            break


            #check if game ended
            if len(self.projectiles) <= 0:
                playAgain = False
                if len(self.bubbles) <= 0:
                    self.writeToScreen(center, "You won!", True)
                    gameOver = True
                    break

                elif self.touchesLeft <= 0:
                    gameOver = True
                    hint = True

            # update whole screen
            pygame.display.flip()

            # fill background
            self.win.fill((0, 0, 0))

        if not hint and self.checkReturnToMenu():
            return "Main menu"


        self.writeToScreen(center, "Game over :(", True)
        self.writeToScreen((center[0], center[1] + 100), "H - Hint", False)
        self.writeToScreen((center[0], center[1] + 60), "Would you like to play again? (y/n)", False)
        while(hint):

            input = self.checkInputs([pygame.K_h, pygame.K_y, pygame.K_n])

            if input == pygame.K_h:
                moves = self.solution
                self.writeToScreen(center, "HINT", True)
                self.writeToScreen((center[0], center[1] - 40), "[row, column]", True)
                self.writeToScreen((center[0], center[1]), "Solution: ", True)
                position = 40

                for move in moves:
                    self.writeToScreen((center[0], center[1] + position), str(move), False)
                    position += 40
                    pygame.display.flip()

                self.writeToScreen((center[0], center[1] + position), "Would you like to play again? (y/n)", False)


            if input == pygame.K_y:
                return "Play again"

            if input == pygame.K_n:
                pygame.quit()
                quit()

            pygame.display.flip()


    #logic for computer mode
    def playComputer(self):
        gameOver = False
        greedy = False
        moves = []
        waitingForSelection = True
        self.ai = AI(self.startGrid, self.touchesLeft)

        #Select AI mode
        while waitingForSelection:
            waitingForSelection = False
            self.writeToScreen(center, "Press A to BFS algorithm", True)
            self.writeToScreen((center[0], center[1] + 40), "Press B to DFS algorithm", False)
            self.writeToScreen((center[0], center[1] + 80), "Press C to IDDFS algorithm", False)
            self.writeToScreen((center[0], center[1] + 120), "Press D to Greedy algorithm", False)
            pygame.display.flip()

            input = self.checkInputs([pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d])

            #choose algo to use
            if input == pygame.K_a:
                moves = self.ai.BFS()

            elif input == pygame.K_b:
                moves = self.ai.dfs()

            elif input == pygame.K_c:
                moves = self.ai.iddfs_algorithm()

            elif input == pygame.K_d:
                greedy = True

            else:
                waitingForSelection = True

            print(len(moves))
            print(self.touchesLeft)
            #check if algo returned solution with more moves than allowed
            if len(moves) > self.touchesLeft:
                self.writeToScreen(center, "No solution exists for given moves :(", True)
                pygame.display.flip()
                gameOver = True


        #choose heuristic for greedy mode
        while(greedy):
            self.writeToScreen(center, "Press A to Level Heuristic", True)
            self.writeToScreen((center[0], center[1] + 40), "Press B to Score Heuristic", False)
            pygame.display.flip()

            input = self.checkInputs([pygame.K_a, pygame.K_b])

            if input == pygame.K_a:
                moves = self.ai.greedy_algorithm("levels")
                greedy = False

            if input == pygame.K_b:
                moves = self.ai.greedy_algorithm("score")
                greedy = False

            #check if algo returned solution with more moves than allowed
            if len(moves) > self.touchesLeft:
                self.writeToScreen(center, "No solution exists for given moves :(", True)
                pygame.display.flip()
                gameOver = True

        if not gameOver:
            waitBetweenMoves = False
            self.win.fill((0, 0, 0))
            pygame.display.flip()
            self.update()
            pygame.time.wait(1000)

        print(moves)

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

                        #if the bubble isn't going to explode, wait 1 second to see the changes on screen
                        if bubble.level > 1:
                            waitBetweenMoves = True

                        self.makeMove(bubble)
                        self.touchesLeft -= 1
                        break

            #check if game ended
            if len(self.projectiles) <= 0:
                if len(self.bubbles) <= 0:
                    self.writeToScreen(center, "You won!", True)
                    gameOver = True
                    break

                elif self.touchesLeft <= 0 or len(moves) == 0:
                    self.writeToScreen(center, "Game over :(", True)
                    gameOver = True

            # update whole screen
            pygame.display.flip()

            # fill background
            self.win.fill((0, 0, 0))

        if self.checkReturnToMenu():
            return "Main menu"


    # write text in the screen, if clearScreen=true, whole screen is wiped before writing
    def writeToScreen(self, pos, text, clearScreen):
        if clearScreen:
            self.win.fill((0, 0, 0))

        smallfont = pygame.font.SysFont("Arial", 25)
        textSurf = smallfont.render(text, True, (255, 255, 255))
        textRect = textSurf.get_rect()
        textRect.center = pos
        self.win.blit(textSurf, textRect)

    # checks collision between sprites, removes projectiles which hit balls, returns score increment
    def checkCollisions(self):
        # dictionary with bubbles and projectiles which collided
        ballsHit = groupcollide(self.bubbles, self.projectiles, False, True)
        scoreAddition = 0

        #hit bubbles which have collided with a projectile
        for bubble in ballsHit.keys():
            newExplosion = bubble.hit()

            #if bubble exploded, generate new projectiles
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

    #update entities
    def update(self):
        # update bubbles, projectiles
        self.bubbles.update()
        self.projectiles.update()

        # check collisions between projectiles and bubbles. update score
        self.score += self.checkCollisions()

        # draw all entities
        self.writeToScreen((center[0] - 100, 20), "Score: " + str(self.score), False)
        self.writeToScreen((center[0], windowHeight + 50), "Touches left: " + str(self.touchesLeft), False)
        self.writeToScreen((center[0] + 100, 20), "H - Hint", False)

        self.bubbles.draw(self.win)
        self.projectiles.draw(self.win)
        pygame.display.flip()

