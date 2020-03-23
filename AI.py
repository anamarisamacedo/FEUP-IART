rowNr = 6
colNr = 5

class AI():
    def __init__(self, grid):
        self.grid = grid


    # function for AI to generate moves
    def clickBubble(self, pos):
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
                    self.grid = self.clickBubble((i, col))
                    break

            # burst bubble below
            for i in range(row + 1, rowNr):
                if self.grid[i][col] > 0:
                    # explode next bubble
                    self.grid = self.clickBubble((i, col))
                    break

            # burst bubble left
            for i in range(col - 1, -1, -1):
                if self.grid[row][i] > 0:
                    # explode next bubble
                    self.grid = self.clickBubble((row, i))
                    break

            # burst bubble right
            for i in range(col + 1, colNr):
                if self.grid[row][i] > 0:
                    # explode next bubble
                    self.grid = self.clickBubble((row, i))
                    break

            return self.grid

    # currently just for testing, makes a predefined move
    def BFS(self):
        moves = [(0, 0), (1, 1)]

        for move in moves:
            print(move)
            print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                             for row in self.grid]))

            print("\n")

            self.grid = self.clickBubble(move)

        return moves