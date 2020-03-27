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
            #check mouse events
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
startGrid = []
grid1 = []
grid2 = []



grid1.append([1, 0, 0, 4, 1])
grid1.append([0, 1, 0, 1, 0])
grid1.append([0, 0, 1, 0, 0])
grid1.append([0, 0, 0, 0, 0])
grid1.append([0, 1, 0, 1, 0])
grid1.append([1, 1, 0, 0, 1])

grid2.append([1, 1, 0, 2, 1])
grid2.append([1, 1, 1, 1, 2])
grid2.append([1, 1, 3, 2, 0])
grid2.append([1, 1, 3, 2, 1])
grid2.append([0, 0, 4, 1, 0])
grid2.append([1, 0, 2, 2, 0])

newGrid = [[1, 1, 1, 4, 2], [4, 3, 3, 4, 0], [1, 1, 0, 2, 1], [1, 1, 3, 4, 3], [0, 0, 4, 1, 0], [2, 0, 3, 2, 0]]

startGrid.append([1, 1, 1, 1, 1])
startGrid.append([1, 2, 0, 0, 0])
startGrid.append([1, 0, 0, 0, 0])
startGrid.append([1, 0, 0, 0, 0])
startGrid.append([1, 0, 0, 0, 0])
startGrid.append([1, 0, 0, 0, 0])

def parseLevels(file):
    levels = []
    rawFiile = []
    newLevel = []

    with open(file) as my_file:
        rawFile = my_file.read().splitlines()

    for line in rawFile:
        if line[:-1] == "Level":
            newLevel.clear()
            newLevel.append(line[-1:])
            newLevel.append([])


        elif len(newLevel[1]) < 4:
            newLine = line.split()
            newLevel[1].append(newLine)

            if len(newLevel[1] == 4):
                levels.append(newLevel)

    return levels


newArray = parseLevels("Levels.txt")


print(newArray)



#game(newGrid, touchesLeft)










