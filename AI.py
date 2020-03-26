rowNr = 6
colNr = 5

import numpy as np
import copy


class AI():
    def __init__(self, grid, touchesLeft):
        self.grid = grid
        self.touchesLeft = touchesLeft


    def canCreateProjectile(self, projectile):
        # projectile going up
        if projectile[1] == 1:
            if projectile[0][0] - 1 >= 0:
                projectile[0][0] -= 1
                return True
            else:
                return False

        # projectile going right
        elif projectile[1] == 2:
            if projectile[0][1] + 1 <= colNr - 1:
                projectile[0][1] += 1
                return True
            else:
                return False

        # projectile going down
        elif projectile[1] == 3:
            if projectile[0][0] + 1 <= rowNr - 1:
                projectile[0][0] += 1
                return True
            else:
                return False

        # projectile going left
        elif projectile[1] == 4:
            if projectile[0][1] - 1 >= 0:
                projectile[0][1] -= 1
                return True
            else:
                return False

        else:
            return True


    def clickBubble(self, state, pos):
        #projectiles= [pos, direction]
        projectiles = [[list(pos), 0]]

        grid = copy.deepcopy(state)

        while len(projectiles) > 0:
            #updates projectiles position, and removes the ones that go off grid
            projectiles[:] = [projectile for projectile in projectiles if self.canCreateProjectile(projectile)]

            #set containing balls which have been hit
            ballsHit = set()

            #collide projectiles with balls
            for projectile in projectiles:

                #if there is a ball in the projectiles position
                if grid[projectile[0][0]][projectile[0][1]] > 0:
                    ballsHit.add((projectile[0][0], projectile[0][1]))
                    projectiles.remove(projectile)

            for ballPos in ballsHit:

                #if it's a level 1 ball, create new projectiles
                if grid[ballPos[0]][ballPos[1]] == 1:

                    for i in range(1, 5):
                        projectiles.append([list(ballPos), i])

                grid[ballPos[0]][ballPos[1]] -= 1

        return grid





    def BFS(self):
        # candidates = [grid, list of moves]
        candidates = [[copy.deepcopy(self.grid), []]]

        while True:
            candidate = candidates.pop(0)

            newCandidates = self.expand(candidate)

            if self.isSolution(candidate[0]):
                print(candidate)
                return candidate[1]
            else:
               candidates.extend(newCandidates)


    def validate_movement(self, row, col, state):
        return (col >= 0 and col <= 5 and row >= 0 and row <= 6 and state[row][col] != 0)

    def execute_movement(self, state, row, col):
        return self.clickBubble(state, [row, col])

    def evaluate_movement_levels(self, new_state):
        return np.sum(new_state)

    def evaluate_movement_score(self, new_state):
        return

    def isSolution(self, new_state):
        return np.sum(new_state) == 0

    def expand(self, node):
        next_nodes = []

        for row in range(0, rowNr):
            for col in range(0, colNr):
                if node[0][row][col] > 0:
                    new_grid = self.execute_movement(node[0], row, col)
                    new_moves = copy.deepcopy(node[1])
                    new_moves.append([row, col])

                    next_nodes.append([new_grid, new_moves])

        return next_nodes

    def dfs(self, limit=5):
        node = [copy.deepcopy(self.grid), []]
        stack = [node]

        # to control depth
        SENTINEL = object()

        while stack:
            node = stack.pop()

            if self.isSolution(node[0]):
                return node[1]

            elif node == SENTINEL:
                # finished this depth-level, go back one level
                limit += 1

            elif limit != 0:
                # goind one level deeper, must push sentinel
                limit -= 1
                next_nodes = self.expand(node)
                stack.append(SENTINEL)
                stack.extend(next_nodes)

    def iddfs_algorithm(self):
        max_depth = copy.deepcopy(self.touchesLeft)
        state = copy.deepcopy(self.grid)
        for depth in range(0,max_depth):
            result = self.iddfs([[state,[]]], depth)
            if result is None:
                continue
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

                    state_move_list.insert(0,[children, all_moves])

                    result = self.iddfs(state_move_list, depth - 1)
                    if result is not None and self.isSolution(result[0]):
                        return result


    def greedy_algorithm(self):
        movfin = []
        state = copy.deepcopy(self.grid)
        touchesLeft = copy.deepcopy(self.touchesLeft)
        return self.greedy_levels(state, movfin, touchesLeft)

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
        aval = 0
        for row in range(0, rowNr):
            for col in range(0, colNr):
                if (self.validate_movement(row, col, state)):
                    new_state = copy.deepcopy(self.execute_movement(state, row, col))
                    if (self.evaluate_movement_score(new_state) > aval):
                        aval = copy.deepcopy(self.evaluate_movement(new_state))
                        move = [row, col]
        movfin.append(move)
        toques -= 1
        if (toques == 0 or self.isSolution(new_state)):
            print(movfin)
            return movfin
        self.greedy(new_state, movfin, toques)
