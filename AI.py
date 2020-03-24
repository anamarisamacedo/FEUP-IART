rowNr = 6
colNr = 5

import numpy as np
import copy

class AI():
    def __init__(self, grid, touchesLeft):
        self.grid = grid
        self.touchesLeft = touchesLeft

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


    def validate_movement(self, row, col, state):
        return (col >= 0 and col <= 5 and row >= 0 and row <= 6 and state[row][col] != 0)

    def execute_movement(self, state, row, col):
        return self.clickBubble(state, [row, col])

    def evaluate_movement_levels(self, new_state):
        return np.sum(new_state)

    def evaluate_movement_score(self, new_state):
        return

    def isSolution(self, new_state):
        return (np.sum(new_state) == 0)

    def dfs_algorithm(self):
        return

    def iddfs_algorithm(self):
        max_depth = copy.deepcopy(self.touchesLeft)
        state = copy.deepcopy(self.grid)
        for depth in range(0,max_depth):
            moves = self.iddfs([state], depth)
            if moves is None:
                continue
            return moves

    def iddfs(self, moves_list, depth):
        current_state = moves_list[-1]
        if (self.isSolution(current_state)):
            return True
        if depth <= 0:
            return None

        for edge in current_state.children:
            new_moves_list = list(moves_list)
            #new_moves_list.append(edge.)
            result = self.iddfs(new_moves_list, depth - 1)
            if result is not None:
                return result

    def greedy_algorithm(self):
        movfin = []
        state = copy.deepcopy(self.grid)
        touchesLeft = copy.deepcopy(self.touchesLeft)
        moves = self.greedy_levels(state, movfin, touchesLeft)
        return moves

    def greedy_levels(self, state, movfin, toques):
        aval = 1000
        for row in range(0, rowNr):
            for col in range(0, colNr):
                if (self.validate_movement(row, col, state)):
                    new_state = copy.deepcopy(self.execute_movement(state, row, col))
                    if (self.evaluate_movement_levels(new_state) < aval):
                        aval = copy.deepcopy(self.evaluate_movement_levels(new_state))
                        move = copy.deepcopy([row, col])
        movfin.append(move)
        toques -= 1
        if (toques == 0 or self.isSolution(new_state)):
            print(movfin)
            return movfin
        return self.greedy_levels(new_state, movfin, toques)


    def greedy_score(self, movfin, toques, score):
        state = copy.deepcopy(self.grid)
        aval = 1000
        for row in range(0, rowNr):
            for col in range(0, colNr):
                if (self.validate_movement(row, col, state)):
                    new_state = copy.deepcopy(self.execute_movement(state, row, col))
                    if (self.evaluate_movement_score(new_state) < aval):
                        aval = copy.deepcopy(self.evaluate_movement(new_state))
                        move = [row, col]
        movfin.append(move)
        toques -= 1
        if (toques == 0 or self.isSolution(new_state)):
            print(movfin)
            return movfin
        self.greedy(new_state, movfin, toques)

