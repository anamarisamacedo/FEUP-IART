rowNr = 6
colNr = 5

import numpy as np
import copy

class AI():
    def __init__(self, grid):
        self.grid = grid


    # function for AI to generate moves
    def clickBubble(self, grid, pos):
        row = pos[0]
        col = pos[1]
        state = copy.deepcopy(grid)

        if state[row][col] == 0:
            return state

        elif state[row][col] > 1:
            state[row][col] -= 1
            return state

        else:
            state[row][col] -= 1
            # burst bubble above
            for i in range(row - 1, -1, -1):
                if state[i][col] > 0:
                    # explode next bubble
                    state = self.clickBubble(state, (i, col))
                    break

            # burst bubble below
            for i in range(row + 1, rowNr):
                if state[i][col] > 0:
                    # explode next bubble
                    state = self.clickBubble(state, (i, col))
                    break

            # burst bubble left
            for i in range(col - 1, -1, -1):
                if state[row][i] > 0:
                    # explode next bubble
                    state = self.clickBubble(state, (row, i))
                    break

            # burst bubble right
            for i in range(col + 1, colNr):
                if state[row][i] > 0:
                    # explode next bubble
                    state = self.clickBubble(state, (row, i))
                    break

            return state

    def BFS(self):
        #candidates = [grid, list of moves]
        candidates = [[copy.deepcopy(self.grid), [] ]]

        while True:
            newCandidates = []

            for candidate in candidates:
                for row in range(0, rowNr):
                    for col in range(0, colNr):

                        if candidate[0][row][col] > 0:

                            newGrid = self.execute_movement(candidate[0], row, col)
                            newMoves = copy.deepcopy(candidate[1])
                            newMoves.append([row, col])

                            candidates.append([newGrid, newMoves])

                            if self.isSolution(newGrid):
                                return newMoves

            candidates = copy.deepcopy(newCandidates)


    def validate_movement(self, col, row, state):
        return (col >= 0 and col <= 5 and row >= 0 and row <= 6 and state[row][col] != 0)

    def execute_movement(self, state, row, col):
        return self.clickBubble(state, (row, col))

    def evaluate_movement(self, new_state):
        return np.sum(new_state)

    def isSolution(self, new_state):
        return (np.sum(new_state) == 0)

    def iddfs_algorithm(self, grid, toques):
        max_depth = toques
        self.iddfs(grid, toques, max_depth, max_depth)

    def iddfs(self, state, toques, depth, max_depth):
        if (self.isSolution(state)):
            return True

        depth += 1
        if (depth == max_depth):
            return False

        # iddfs(stateVizinho, toques)

    def greedy_algorithm(self, state, toques):
        movfin = []
        return self.greedy(state, movfin, toques)

    def greedy(self, state, movfin, toques):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in state]))
        aval = 1000
        for i in range(0, colNr):
            for j in range(0, rowNr):
                if (self.validate_movement(i, j, state)):
                    new_state = self.execute_movement(state, j, i)
                    if (self.evaluate_movement(new_state) < aval):
                        aval = self.evaluate_movement(new_state)
                        move = (i, j)
        movfin.append(move)
        toques -= 1
        if (toques == 0 or self.isSolution(new_state)):
            print(movfin)
            return movfin
        self.greedy(new_state, movfin, toques)