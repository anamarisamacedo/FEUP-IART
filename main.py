from game import *

#currently just for testing, makes a predefined move
def BFS(grid):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in grid]))

    print("\n")

    grid = clickBubble(grid, (1, 3))

    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in grid]))

    return [(0, 1), (1, 3)]

def validate_movement(col, row, state):
    return (col >= 0 and col <=5 and row >= 0 and row <=6 and state[row][col] != 0)

def execute_movement(state,col,row):
    return clickBubble(state, (row,col))

def evaluate_movement(new_state):
    return np.sum(new_state)

def jogo_terminado(new_state):
    return (np.sum(new_state)==0)

def iddfs_algorithm(grid, toques):
    max_depth=toques
    iddfs(grid, toques, max_depth, max_depth)

def iddfs(state, toques, depth, max_depth):
    if(jogo_terminado(state)):
        return True

    depth +=1
    if(depth== max_depth):
        return False

    #iddfs(stateVizinho, toques)

def greedy_algorithm(state, toques):
    movfin=[]
    return greedy(state,movfin, toques)

def greedy(state,movfin, toques):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in state]))
    aval=1000
    for i in range(0, colNr):
        for j in range(0, rowNr):
            if(validate_movement(i,j,state)):
                new_state = execute_movement(state,i,j)
                if (evaluate_movement(new_state) < aval):
                    aval= evaluate_movement(new_state)
                    move = (i,j)
    movfin.append(move)
    toques -= 1
    if(toques == 0 or jogo_terminado(new_state)):
        print(movfin)
        return movfin
    greedy(new_state, movfin, toques,)

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

                if event.type == pygame.KEYDOWN:
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
