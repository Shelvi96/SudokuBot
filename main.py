import time
from selenium import webdriver


class SudokuSolver:

    def __init__(self, board):
        self.board = board

    def getBoard(self):
        return self.board

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False

    def valid(self, num, pos):
        # Check row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check x
        boardx_x = pos[1] // 3
        boardx_y = pos[0] // 3

        for i in range(boardx_y * 3, boardx_y * 3 + 3):
            for j in range(boardx_x * 3, boardx_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False
        return True

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return i, j  # row, col
        return None


class SudokuBot:

    def __init__(self):
        self.board = []
        self.difficulty = {
            "Easy": "g1",
            "Medium": "g2",
            "Hard": "g3",
            "Very Hard": "g4"
        }
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.sudokukingdom.com/')
        time.sleep(1)

    def setDifficulty(self, level):
        val = self.driver.find_element_by_xpath("//div[@id=\"{}\"]".format(self.difficulty[level]))
        val.click()
        time.sleep(1)

    def readBoard(self):
        for i in range(0, 9):
            list = []
            for j in range(0, 9):
                val = self.driver.find_element_by_xpath("//div[@id=\"vc_{}_{}\"]".format(j, i))
                if val.text == "":
                    list.append(0)
                else:
                    list.append(int(val.text))
            self.board.append(list)

    def findSolution(self):
        solver = SudokuSolver(self.board)
        solver.solve()
        self.board = solver.getBoard()

    def writeSolution(self):
        for i in range(0, 9):
            for j in range(0, 9):
                val = self.driver.find_element_by_xpath("//div[@id=\"vc_{}_{}\"]".format(j, i))
                if val.text == "":
                    num = self.driver.find_element_by_xpath("//div[@id=\"M{}\"]".format(self.board[i][j]))
                    num.click()
                    time.sleep(0.25)
                    val.click()
                    time.sleep(0.25)

    def solveSudoku(self):
        self.readBoard()
        self.findSolution()
        self.writeSolution()


if __name__ == '__main__':
    bot = SudokuBot()
    bot.setDifficulty("Very Hard")
    bot.solveSudoku()
