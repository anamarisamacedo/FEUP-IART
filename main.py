from game import *
from collections import deque


# Project main loop
def game(levels):
    game = Game(levels)

    intro = run = True
    computer = human = choosingLevel = False

    while run:
        #MAIN MENU
        while intro:

            game.writeToScreen(center, "Press H to play in human mode. ", True)
            game.writeToScreen((center[0], center[1] + 30), "Press C to play in computer mode. ", False)
            pygame.display.flip()

            input = game.checkInputs([pygame.K_h, pygame.K_c])
            # check mouse events
            if input == pygame.K_h:
                human = True
            if input == pygame.K_c:
                computer = True

            if input == "quit":
                pygame.quit()

            if (human or computer):
                intro = False
                choosingLevel = True
                game.writeToScreen(center, "", True)


        levelNotChosen = True

        #choose level to play
        while choosingLevel:
            if levelNotChosen:
                game.writeToScreen(center, "What level would you like to play?", False)
                game.writeToScreen((center[0], center[1] + 50), "Select from 1 to " + str(len(levels)), False)

            pygame.display.flip()
            # check mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                #check level chosen
                elif event.type == pygame.KEYDOWN:
                    level = pygame.key.name(event.key)

                    if level >= '1' and level <= str(len(levels)):
                        game.setLevel(int(level))
                        choosingLevel = False
                    else:
                        game.writeToScreen((center[0], center[1] - 50), "That level doesn't exist", False)
                        levelNotChosen = True

        selection = ""
        if(human):
            while True:
                selection = game.playHuman()
                if selection == "Main menu":
                    intro = run = True
                    computer = human = choosingLevel = False
                    break

                if selection == "Play again":
                    game = Game(levels)
                    game.setLevel(int(level))

        elif(computer):
            while True:
                selection = game.playComputer()
                if selection == "Main menu":
                    intro = run = True
                    computer = human = choosingLevel = False
                    break


        while selection != "Main menu":
            # check mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()



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
    rawFile = []
    newLevel = []
    wroteLevel = wroteTouches = wroteSol = False

    with open(file) as my_file:
        rawFile = my_file.read().splitlines()

    for line in rawFile:
        if not wroteLevel:
            newLevel.clear()
            newLevel.append(int(line[-1:]))
            newLevel.append([])
            newLevel.append([])
            newLevel.append([])
            wroteLevel = True

        elif not wroteTouches:
            newLevel[2] = int(line)
            wroteTouches = True

        elif not wroteSol:
            sol = line.split(';')
            for move in sol:
                newLevel[3].append(list(map(int, move.split(","))))
            wroteSol = True

        elif len(newLevel[1]) < 6:
            newLine = list(map(int, line.split()))
            newLevel[1].append(newLine)

            if len(newLevel[1]) == 6:
                levels.append(copy.deepcopy(newLevel))
                wroteLevel = wroteTouches = wroteSol = False

    return levels

game(parseLevels("Levels.txt"))












