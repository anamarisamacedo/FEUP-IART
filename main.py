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



touchesLeft = 10
startGrid = []


'''
# lvl 10, 1 touch, solved by dfs
startGrid.append([2, 2, 2, 2, 2])
startGrid.append([2, 1, 2, 1, 2])
startGrid.append([2, 0, 1, 0, 2])
startGrid.append([2, 0, 1, 0, 2])
startGrid.append([2, 1, 3, 1, 2])
startGrid.append([2, 2, 2, 2, 2])

'''
'''
# lvl 50, 4 touches
startGrid.append([3, 1, 4, 3, 4])
startGrid.append([3, 4, 0, 3, 3])
startGrid.append([1, 4, 1, 2, 1])
startGrid.append([2, 1, 1, 1, 1])
startGrid.append([1, 0, 4, 4, 4])
startGrid.append([1, 0, 2, 4, 1])



'''
# grid lvl 70, 5 touches, solved by dfs
startGrid.append([1, 3, 3, 2, 0])
startGrid.append([1, 4, 1, 0, 3])
startGrid.append([0, 0, 1, 0, 1])
startGrid.append([4, 1, 0, 2, 4])
startGrid.append([3, 4, 2, 1, 0])
startGrid.append([1, 0, 2, 0, 4])


game(startGrid, touchesLeft)


# candidates = [{'grid': startGrid, 'moves': [[1, 2], [1, 2], [1, 2]]}]
#
# for candidate in candidates:
#     newGrid = copy.deepcopy(candidate['grid'])