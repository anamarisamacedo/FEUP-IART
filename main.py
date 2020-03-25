import pygame as pygame

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



touchesLeft = 5
startGrid= []

'''
startGrid.append([1, 1, 1, 1, 2])
startGrid.append([1, 1, 3, 2, 0])
startGrid.append([1, 1, 0, 2, 1])
startGrid.append([1, 1, 3, 2, 1])
startGrid.append([0, 0, 4, 1, 0])
startGrid.append([1, 0, 2, 2, 0])

startGrid.append([1, 0, 0, 4, 1])
startGrid.append([0, 1, 0, 1, 0])
startGrid.append([0, 0, 1, 0, 0])
startGrid.append([0, 0, 0, 0, 0])
startGrid.append([0, 1, 0, 1, 0])
startGrid.append([1, 1, 0, 0, 1])
'''


startGrid.append([0, 0, 0, 0, 0])
startGrid.append([0, 0, 0, 0, 0])
startGrid.append([0, 0, 0, 0, 0])
startGrid.append([0, 0, 0, 0, 0])
startGrid.append([1, 1, 0, 0, 0])
startGrid.append([1, 1, 1, 3, 0])
Ai = AI(startGrid, 5)

print(Ai.execute_movement(startGrid, 4, 0))
#nextGrid = Ai.execute_movement(startGrid, 0, 0)
#print(Ai.execute_movement(nextGrid, 2, 1))
game(startGrid, touchesLeft)

#newGrid = [[1, 1, 1, 1, 1], [4, 2, 3, 1, 2], [2, 1, 4, 1, 1], [3, 0, 1, 3, 0], [2, 1, 0, 4, 3], [0, 3, 2, 3, 1]]
#game(newGrid, touchesLeft)

#
# candidates = [{'grid': startGrid, 'moves': [[1, 2], [1, 2], [1, 2]]}]
#
# for candidate in candidates:
#     newGrid = copy.deepcopy(candidate['grid'])