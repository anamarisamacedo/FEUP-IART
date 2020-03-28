rowNr = 6
colNr = 5

import numpy as np
import copy


class AI():
    def __init__(self, grid, touchesLeft):
        self.grid = grid
        self.touchesLeft = touchesLeft
        self.score = 0

    #returns true if the next position for the projectile is valid
    def updateProjectile(self, projectile):
        #Update projectile position
        projectile[0][0] += projectile[1][0]
        projectile[0][1] += projectile[1][1]
        return self.isValidPos(projectile[0][0], projectile[0][1])


    #clicks bubble at pos, returns new grid with the next state
    def clickBubble(self, state, pos):
        #projectile list at the current moment, initialized with a projectile in the click position
        #projectiles= [pos, direction]
        projectiles = [[list(pos), [0, 0]]]

        #list of projectiles that hit a ball
        projectilesHit = []

        grid = copy.deepcopy(state)

        while len(projectiles) > 0:
            #updates projectiles position, and removes the ones that go off grid
            projectiles[:] = [projectile for projectile in projectiles if self.updateProjectile(projectile)]

            #Creates list of projectiles which hit a ball
            projectilesHit[:] = [projectile for projectile in projectiles if grid[projectile[0][0]][projectile[0][1]] > 0]

            #Updates projectiles list to keep only the ones that didn't hit anything
            projectiles[:] = [projectile for projectile in projectiles if not grid[projectile[0][0]][projectile[0][1]] > 0]

            #set containing balls which have been hit
            ballsHit = set()

            for projectile in projectilesHit:
                ballsHit.add((projectile[0][0], projectile[0][1]))

            for ballPos in ballsHit:
                #if it's a level 1 ball, create new projectiles
                if grid[ballPos[0]][ballPos[1]] == 1:
                    self.score += 10
                    projectiles.append([list(ballPos), [0, 1]])
                    projectiles.append([list(ballPos), [0, -1]])
                    projectiles.append([list(ballPos), [1, 0]])
                    projectiles.append([list(ballPos), [-1, 0]])

                grid[ballPos[0]][ballPos[1]] -= 1

        return grid

    #returns true if pos(row, col) is within the grid
    def isValidPos(self, row, col):
        return (col >= 0 and col < colNr and row >= 0 and row < rowNr)

    #returns true if there is a bubble in (row, col), and (row, col) is within grid
    def validate_movement(self, row, col, state):
        return (self.isValidPos(row, col) and state[row][col] != 0)

    #wrapper function for clickBubble
    def execute_movement(self, state, row, col):
        return self.clickBubble(state, [row, col])

    #returns sum of all the bubbles' levels in the grid (if it returns 0, new_state is solved)
    def evaluate_movement_levels(self, new_state):
        return np.sum(new_state)

    #TODO: should do someting?
    def evaluate_movement_score(self, new_state):
        return

    #returns true if there aren't bubbles in the grid
    def isSolution(self, new_state):
        return np.sum(new_state) == 0

    def printPath(self, path):
        for p in path:
            print(p)

    #returns all possible moves for given grid
    def expand(self, node):
        next_nodes = []

        for row in range(0, rowNr):
            for col in range(0, colNr):
                if self.validate_movement(row, col, node[0]):
                    new_grid = self.execute_movement(node[0], row, col)
                    new_moves = copy.deepcopy(node[1])
                    new_moves.append([row, col])

                    next_nodes.append([new_grid, new_moves])

        return next_nodes

    def BFS(self):
        # candidate = [grid, list of moves]
        candidates = [[copy.deepcopy(self.grid), []]]

        while True:
            candidate = candidates.pop(0)

            newCandidates = self.expand(candidate)

            if self.isSolution(candidate[0]):
                return candidate[1]
            else:
               candidates.extend(newCandidates)

    def dfs(self):
        limit = self.touchesLeft
        node = [copy.deepcopy(self.grid), []]
        stack = [node]
        path = []

        # to control depth
        SENTINEL = object()

        while stack:
            node = stack.pop()
            self.printPath(stack)

            if node == SENTINEL:
                # finished this depth-level, go back one level
                limit += 1
                path.pop()

            elif self.isSolution(node[0]):
                path.append(node)
                self.printPath(path)
                return node[1]

            elif limit != 0:
                # going one level deeper, must push sentinel
                limit -= 1
                next_nodes = self.expand(node)
                path.append(node)
                stack.append(SENTINEL)
                stack.extend(next_nodes)

        print("No solution found")

    def iddfs_algorithm(self):

        max_depth = self.touchesLeft +1
        #initial state
        state = copy.deepcopy(self.grid)

        for depth in range(0, max_depth):
            result = self.iddfs([[state, []]], depth)
            if result is None:
                continue
            print(result[1])
            return result[1]

    def iddfs(self, state_move_list, depth):
        current_state = state_move_list[0][0]
        moves = state_move_list[0][1]
        if (self.isSolution(current_state)):
            return state_move_list[0]
        if depth <= 0:
            return None

        for row in range(0, rowNr):
            for col in range(0, colNr):
                if self.validate_movement(row, col, current_state):
                    children = self.execute_movement(current_state, row, col)
                    all_moves = copy.deepcopy(moves)
                    all_moves.append([row, col])

                    state_move_list.insert(0, [children, all_moves])

                    result = self.iddfs(state_move_list, depth - 1)

                    if result is not None and self.isSolution(result[0]):
                        return result


    def greedy_algorithm(self, heuristic):
        movfin = []
        state = copy.deepcopy(self.grid)

        if(heuristic == "levels"):
            return self.greedy_levels(state, movfin, self.touchesLeft)
        elif(heuristic == "score"):
            move = self.greedy_score(state, movfin, self.touchesLeft, self.score)
            print(move)
            return move

    def greedy_levels(self, state, movfin, toques):
        aval = 1000

        for row in range(0, rowNr):
            for col in range(0, colNr):
                if (self.validate_movement(row, col, state)):
                    new_state = copy.deepcopy(self.execute_movement(state, row, col))

                    if (self.evaluate_movement_levels(new_state) < aval):
                        best_state= new_state
                        aval = self.evaluate_movement_levels(new_state)
                        move = [row, col]

        movfin.append(move)
        toques -= 1
        if (toques == 0 or self.isSolution(best_state)):
            return movfin
        return self.greedy_levels(best_state, movfin, toques)

    def greedy_score(self, state, movfin, toques, score):
        aval = 0
        move = []
        for row in range(0, rowNr):
            for col in range(0, colNr):

                if (self.validate_movement(row, col, state)):
                    self.score=0
                    new_state = copy.deepcopy(self.execute_movement(state, row, col))
                    totalScore = self.score + score
                    if (totalScore > aval):
                        best_state = new_state
                        aval = totalScore
                        move = [row, col]

        movfin.append(move)
        toques -= 1
        if (toques == 0 or self.isSolution(best_state)):
            print(aval)
            return movfin
        return self.greedy_score(best_state, movfin, toques, aval)
