rowNr = 6
colNr = 5


import numpy as np
import copy
import datetime
from collections import deque


class AI():
    def __init__(self, grid, touchesLeft):
        self.grid = grid
        self.touchesLeft = touchesLeft
        self.score = 0
        self.num_nodes_iddfs = 0

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

    #returns true if there aren't bubbles in the grid
    def isSolution(self, new_state):
        return np.sum(new_state) == 0

    def printPath(self, path):
        for p in path:
            print(p)

    #returns all possible moves, states/childrens and score for given grid
    def expand(self, node):
        next_nodes = []

        for row in range(0, rowNr):
            for col in range(0, colNr):
                if self.validate_movement(row, col, node[0]):
                    self.score = 0
                    new_grid = self.execute_movement(node[0], row, col)
                    new_moves = copy.deepcopy(node[1])
                    new_moves.append([row, col])

                    next_nodes.append([new_grid, new_moves, self.score])

        return next_nodes

    def BFS(self):
        # start time
        start = datetime.datetime.now()

        # solution path
        path = []

        #nodes explored
        num_nodes = 0

        # candidate = [grid, list of moves]
        candidates = deque([[copy.deepcopy(self.grid), []]])

        while True:
            candidate = candidates.popleft()

            num_nodes += 1

            newCandidates = self.expand(candidate)

            if self.isSolution(candidate[0]):
                end = datetime.datetime.now()
                time = end - start
                self.analysis(time, len(candidate[1]), num_nodes, 0)
                return candidate[1]
            else:
               candidates.extend(newCandidates)

            if len(newCandidates) == 0:
                end = datetime.datetime.now()
                time = end - start
                self.analysis(time, len(candidate[1]), num_nodes, 1)
                return [[]]

    # depth first search, limited depth (technically a DLS - depth limited search)
    def dfs(self):
        # start time
        start = datetime.datetime.now()

        # number of max touches (depth)
        limit = self.touchesLeft

        # initial state
        node = [copy.deepcopy(self.grid), []]

        # put root node in stack
        stack = [node]

        # solution path
        path = []

        # to control depth
        SENTINEL = object()

        num_nodes = 1

        while stack:
            node = stack.pop()

            if node == SENTINEL:
                # finished this depth-level, go back one level
                limit += 1
                path.pop()

            elif self.isSolution(node[0]):
                path.append(node)
                # self.printPath(path)
                print(node[1])
                end = datetime.datetime.now()
                time = end - start
                size = len(node[1])
                self.analysis(time, size, num_nodes,0)
                return node[1]

            elif limit != 0:
                # going one level deeper, must push sentinel to mark level
                limit -= 1
                next_nodes = self.expand(node)
                path.append(node)
                stack.append(SENTINEL)
                stack.extend(next_nodes)
                num_nodes += len(next_nodes)

        print("No solution found")

    def iddfs_algorithm(self):
        start = datetime.datetime.now()

        max_depth = self.touchesLeft + 1  #maximum tree depth (number of possible touches at the current level)

        state = copy.deepcopy(self.grid) #initial state

        for depth in range(0, max_depth): #calls dfs algorithms for each maximum depth
            self.num_nodes_iddfs += 1
            result = self.iddfs([state, []], depth) #result = [state,moves]

            if result is None:
                continue
            #for statistics
            end = datetime.datetime.now()
            time = end - start
            size = len(result[1])
            self.analysis(time, size, self.num_nodes_iddfs, 0)
            # return moves
            print(result[1])
            return result[1]

    def iddfs(self, state_moves, depth):
        #state_moves = [state,moves to reach the state]

        current_state = state_moves[0]

        if (self.isSolution(current_state)):
            return state_moves
        if depth <= 0: #if reaches the maximum depth
            return None

        childrens = self.expand(state_moves)
        self.num_nodes_iddfs += len(childrens)
        for children in childrens:
            #calls the dfs algorithm for each children
            result = self.iddfs(children, depth - 1)

            if result is not None and self.isSolution(result[0][0]):
                    return result

    def greedy_algorithm(self, heuristic):
        #initial state
        state = copy.deepcopy(self.grid)
        start = datetime.datetime.now()
        if(heuristic == "levels"):
            result = self.greedy_levels([state,[]], self.touchesLeft, 1)
            end = datetime.datetime.now()
            time = end - start
            size = len(result[0][1])
            num_nodes = result[1]
            self.analysis(time, size, num_nodes, result[2])
            return result[0][1]
        elif(heuristic == "score"):
            result = self.greedy_score([state, []], self.touchesLeft, self.score, 1)
            end = datetime.datetime.now()
            time = end - start
            size = len(result[0][1])
            num_nodes = result[1]
            self.analysis(time, size, num_nodes, result[2])
            return result[0][1]


    def greedy_levels(self, state_moves, toques, num_nodes):
        aval = 1000

        childrens = self.expand(state_moves)
        num_nodes += len(childrens)
        for children in childrens:
            sum_levels = self.evaluate_movement_levels(children[0])
            if (sum_levels < aval):
                best_children= children
                aval = sum_levels

        toques -= 1
        if (self.isSolution(best_children[0])):
            return [best_children,num_nodes, 0]
        if(toques == 0):
            return [best_children, num_nodes, 1]
        return self.greedy_levels(best_children, toques, num_nodes)

    def greedy_score(self, state_moves, toques, score, num_nodes):
        aval = 0

        childrens = self.expand(state_moves)
        num_nodes += len(childrens)

        for children in childrens:
            children_score = children[2]
            totalScore = children_score + score
            if (totalScore > aval):
                best_children = children
                aval = totalScore

        toques -= 1
        if (self.isSolution(best_children[0])):
            return [best_children,num_nodes,0]
        if(toques == 0):
            return [best_children,num_nodes,1]
        return self.greedy_score(best_children, toques, aval, num_nodes)

    def analysis(self, time, size, num_nodes, won_lost):
        now = datetime.datetime.now()
        if(won_lost == 0):
            print(now.strftime("%Y-%m-%d %H:%M: ") + "Solved puzzle in", time.total_seconds(), "seconds", end=" ")
        else:
            print(now.strftime("%Y-%m-%d %H:%M: ") + "Lost puzzle: ", time.total_seconds(), "seconds", end=" ")
        print("in", size, "move(s). The search tree was expanded by", num_nodes, "nodes.")