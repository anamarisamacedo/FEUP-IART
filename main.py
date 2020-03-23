from game import *

# Project main loop
def game(startGrid, touches):
    game = Game(startGrid, touches)

    intro = run = True
    computer = human = False

    while run:
        game.writeToScreen(center, "Press H to play in human mode. ", True)
        game.writeToScreen((center[0], center[1] + 30), "Press C to play in computer mode. ", False)
        pygame.display.flip()

        #MAIN MENU
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        human = True
                    if event.key == pygame.K_c:
                        computer = True

                    intro = False

        if(human):
            game.playHuman()

        elif(computer):
            game.playComputer()


        #wait for user to click exit button
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()



touchesLeft = 3
startGrid= []

# startGrid.append([1, 1, 1, 1, 1])
# startGrid.append([4, 2, 3, 1, 2])
# startGrid.append([2, 1, 4, 1, 2])
# startGrid.append([3, 0, 1, 3, 0])
# startGrid.append([2, 1, 0, 4, 3])
# startGrid.append([0, 3, 2, 3, 1])

startGrid.append([1, 0, 0, 0, 1])
startGrid.append([0, 1, 0, 1, 0])
startGrid.append([0, 0, 0, 0, 0])
startGrid.append([0, 0, 0, 0, 0])
startGrid.append([0, 1, 0, 1, 0])
startGrid.append([1, 0, 0, 0, 1])


game(startGrid, touchesLeft)

# col = 4
#
# colNr = 4
#
# for i in range(col + 1, colNr):
#     print(i)
