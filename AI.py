rowNr = 6
colNr = 5

class AI():
    def __init__(self, grid):
        self.grid = grid


    # function for AI to generate moves
    def clickBubble(self, state, pos):
        row = pos[0]
        col = pos[1]

        if self.grid[row][col] == 0:
            return self.grid

        elif self.grid[row][col] > 1:
            self.grid[row][col] -= 1
            return self.grid

        else:
            self.grid[row][col] -= 1
            # burst bubble above
            for i in range(row - 1, -1, -1):
                if self.grid[i][col] > 0:
                    # explode next bubble
                    self.grid = self.clickBubble(state, (i, col))
                    break

            # burst bubble below
            for i in range(row + 1, rowNr):
                if self.grid[i][col] > 0:
                    # explode next bubble
                    self.grid = self.clickBubble(state, (i, col))
                    break

            # burst bubble left
            for i in range(col - 1, -1, -1):
                if self.grid[row][i] > 0:
                    # explode next bubble
                    self.grid = self.clickBubble(state, (row, i))
                    break

            # burst bubble right
            for i in range(col + 1, colNr):
                if self.grid[row][i] > 0:
                    # explode next bubble
                    self.grid = self.clickBubble(state, (row, i))
                    break

            return self.grid

    # currently just for testing, makes a predefined move
    def BFS(self):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in self.grid]))
        print("\n")

        grid = self.clickBubble(self.grid, (1, 3))

        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in self.grid]))

        return [(0, 0), (1, 1)]

    def validate_movement(self, col, row, state):
        return (col >= 0 and col <= 5 and row >= 0 and row <= 6 and state[row][col] != 0)

    def execute_movement(self, state, col, row):
        return self.clickBubble(state, (row, col))

    def evaluate_movement(self, new_state):
        return self.np.sum(new_state)

    def jogo_terminado(self, new_state):
        return (self.np.sum(new_state) == 0)

    def iddfs_algorithm(self, grid, toques):
        max_depth = toques
        self.iddfs(grid, toques, max_depth, max_depth)

    def iddfs(self, state, toques, depth, max_depth):
        if (self.jogo_terminado(state)):
            return True

        depth += 1
        if (depth == max_depth):
            return False

        # iddfs(stateVizinho, toques)

    def greedy_algorithm(self, state, toques):
        movfin = []
        return self.greedy(self, state, movfin, toques)

    def greedy(self, state, movfin, toques):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in state]))
        aval = 1000
        for i in range(0, colNr):
            for j in range(0, rowNr):
                if (self.validate_movement(i, j, state)):
                    new_state = self.execute_movement(state, i, j)
                    if (self.evaluate_movement(new_state) < aval):
                        aval = self.evaluate_movement(new_state)
                        move = (i, j)
        movfin.append(move)
        toques -= 1
        if (toques == 0 or self.jogo_terminado(new_state)):
            print(movfin)
            return movfin
        self.greedy(new_state, movfin, toques, )