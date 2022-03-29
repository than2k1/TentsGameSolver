
import copy
import sys

board = []
rowTents = {}
colTents = {}
rowCount = {}
colCount = {}



def readFile(filename):
    global rowTents, colTents, board
    # print(sys.argv[1])
    f = open(filename, 'r')
    count = 0
    f.readline()
    line = f.readline().strip().split("x")
    for i in range(0,int(line[0])):
        row = []
        for j in range(0,int(line[1])):
            row += ["?"]
        board += [row]
    for each in range(0, len(board)):
        rowCount[each] = 0
        colCount[each] = 0
    f.readline()
    while(True):
        line = f.readline().strip()
        if(line == "Columns"):
            break
        else:
            rowTents[count] = int(line)
            count += 1
    count = 0
    while (True):
        line = f.readline().strip()
        if (line == "Trees"):
            break
        else:
            colTents[count] = int(line)
            count += 1
    while(True):
        line = f.readline().strip()
        if(line == ""):
            break
        else:
            line = line.split(",")
            board[int(line[0])][int(line[1])] = "O"
    f.close()

def printBoard():
    print()
    border = "  * * " + "* "*len(board[0])
    count = 0
    bottom = ""
    print(border)
    for row in board:
        toPrint = ""
        for col in row:
            toPrint += col + " "
        print(str(rowTents[count]) + " * " + toPrint + "*")
        bottom += str(colTents[count]) + " "
        count += 1
    print(border)
    print("    " + bottom + " ")
    print()

def isValid(row, col):
    if(isValidSum(row, col) and isValidParity(row,col) and noAdjTents(row, col)):
        return True
    return False

#check if the new tent excess the total
def isValidSum(row, col):
    if rowCount[row] + 1 > rowTents[row]:
        return False
    if colCount[col] + 1 > colTents[col]:
        return False
    return True

#check all neighbors of the tent
def noAdjTents(row, col):
    neighbors = findAllNeighbors(row, col)
    for neighbor in neighbors:
        if board[neighbor[0]][neighbor[1]] == "X":
            return False
    return True

#check 1 to 1 realation of tent and tree
def isValidParity(x,y):
    parity = -1
    pred = [(x,y)]
    for each in findNeighbors(x,y):
        parity += countTreesRec(each[0], each[1], pred)

    if(parity >= 0):
        return True
    else:
        return False

def countTreesRec(x,y, pred):
    pred += [(x,y)]
    if(board[x][y] == "O"):
        parity = 1
        for each in findNeighbors(x,y):
            if(each not in pred):
                parity += countTentsRec(each[0],each[1], pred)
        return parity
    else:
        return 0


def countTentsRec(x,y, pred):
    pred += [(x,y)]
    if (board[x][y] == "X"):
        parity = -1
        for each in findNeighbors(x, y):
            if (each not in pred):
                parity += countTreesRec(each[0], each[1], pred)
        return parity
    else:
        return 0

def findNeighbors(row, col):
    neighbors = []
    if row > 0:
        neighbors += [(row - 1, col)]
    if row < len(board) - 1:
        neighbors += [(row + 1, col)]
    if col > 0:
        neighbors += [(row, col - 1)]
    if col < len(board[0]) - 1:
        neighbors += [(row, col + 1)]
    return neighbors

def findAllNeighbors(row,col):
    neighbors = findNeighbors(row,col)
    if row > 0 and col > 0:
        neighbors += [(row - 1, col - 1)]
    if col < len(board[0]) - 1 and row < len(board) - 1:
        neighbors += [(row + 1, col + 1)]
    if row < len(board) - 1 and col > 0:
        neighbors += [(row + 1, col - 1)]
    if col < len(board[0]) - 1 and row > 0:
        neighbors += [(row - 1, col + 1)]
    return neighbors

def isGoal():
    totalRowTents = 0
    totalColTents = 0

    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            if board[row][col] == "X":
                totalRowTents += 1
        if (totalRowTents != rowTents[row]):
            return False
        else:
            totalRowTents = 0

    for col in range(0, len(board[0])):
        for row in range(0, len(board)):
            if board[row][col] == "X":
                totalColTents += 1
        if (totalColTents != colTents[col]):
            return False
        else:
            totalColTents = 0

    return True


def saveData():
    return (copy.deepcopy(board),
            copy.deepcopy(rowTents),
            copy.deepcopy(colTents),
            copy.deepcopy(rowCount),
            copy.deepcopy(colCount))



def restorData(metadata):
    global board, rowTents, colTents, rowCount, colCount
    board, rowTents, colTents, rowCount, colCount = metadata

def DFS():
    for row in range(len(board)):
        for col in range(len(board[0])):
            
            if board[row][col] == "?":
                data = saveData()
                if isValid(row, col):
                    board[row][col] = "X"
                    if isGoal():
                        # replace all ? with grass
                        for row in range(len(board)):
                            for col in range(len(board[0])):
                                if board[row][col] == "?": board[row][col] = "."
                        return True
                else:
                    board[row][col] = "." #grass
                res = DFS()
                if res:
                    return True
                else:
                    restorData(data)


def nonAdjaToTree():
    #mark  all none tree  adjacent cell with grass
    #tree is O
    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            if board[row][col] != "O":
                board[row][col] = "."
                neighbors = findNeighbors(row, col)
                for neighbor in neighbors:
                    if board[neighbor[0]][neighbor[1]] == "O":
                        board[row][col] = "?"
                        break



def fillInBoard():
    knowInRow = 0
    knowInCol = 0
    filled = False
    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            if board[row][col] == "." or board[row][col] == "O": #grass or tree
                knowInRow += 1
            if (rowTents[row] == 0 or rowCount[row] == rowTents[row]) and board[row][col] != "O" and board[row][col] != "X": 
                board[row][col] = "."
        if len(board[0]) - knowInRow == rowTents[row]:
            for i in range(0, len(board[0])):
                if board[row][i] == "?":
                    board[row][i] = "X"
                    rowCount[row] += 1
                    colCount[i] += 1
                    markAdjaToTent(row,i)
                    filled = True
        knowInRow = 0
    
    for col in range(0, len(board[0])) :
        for row in range(0, len(board)):
            if board[row][col] == "." or board[row][col] == "O": #grass or tree
                knowInCol += 1
            if (colTents[col] == 0 or colTents[col] == colCount[col]) and board[row][col] != "O" and board[row][col] != "X": 
                board[row][col] = "."
        if len(board) - knowInCol == colTents[col]:
            for i in range(0, len(board)):
                if board[i][col] == "?":
                    board[i][col] = "X"
                    colCount[col] += 1
                    rowCount[i] += 1
                    markAdjaToTent(i,col)
                    filled = True
        knowInCol = 0
    return filled
    
def findUnknown():
    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            if board[row][col] == "?":
                return (row, col)
    return None

def solve():
    # printBoard()
    nonAdjaToTree()
    # printBoard()
    run = True
    while run:
        run = fillInBoard()
    # printBoard()
    next = findUnknown()
    if next is not None:
        return solveRec(next[0], next[1])
    else:
        if isGoal():
            return True
        else:
            return None

def solveRec(x,y):
    data = saveData()
    if isValid(x,y):
        board[x][y] = "X" #mark as tent
        colCount[y] += 1
        rowCount[x] += 1
        # printBoard()
        #mark all adja to tent is grass
        markAdjaToTent(x,y)
        # printBoard()
        markRowCol(x,y)
        # printBoard()
        next = findUnknown()
        if next is not None:
            if solveRec(next[0],next[1]) == True:
                return True
            else:
                restorData(data)
                board[x][y] = "."
                if solveRec(next[0],next[1]) == True:
                    return True
                else: return None
        else:
            if isGoal():
                return True
            else: return None
    else:
        board[x][y] = "."
        next = findUnknown()
        if next is not None:
            if solveRec(next[0],next[1]) == True:
                return True
            else:
                restorData(data)
                board[x][y] = "."
                if solveRec(next[0],next[1]) == True:
                    return True
                else: return None
        else:
            if isGoal():
                return True
            else: return None


def markAdjaToTent(row, col):
    neighbors = findAllNeighbors(row, col)
    for neighbor in neighbors:
        if board[neighbor[0]][neighbor[1]] != "O":
            board[neighbor[0]][neighbor[1]] = "."

def markRowCol(row, col):
    knowInCol = 0
    knowInRow = 0
    for column in range(len(board[0])):
        if board[row][column] == "O" or board[row][column] == "." :
            knowInRow += 1
    if knowInRow == len(board[0]) - (rowTents[row] - rowCount[row]):
        for column in range(len(board[0])):
            if board[row][column] == "?":
                board[row][column] = "X"
                colCount[column] += 1
                rowCount[row] += 1
                markAdjaToTent(row,column)
    if rowTents[row] == rowCount[row]:
        for column in range(len(board[0])):
            if board[row][column] == "?":
                board[row][column] = "."
    
    for r in range(len(board)):
        if board[r][col] == "O" or board[r][col] == "." :
            knowInCol += 1
    if knowInCol == len(board) - (colTents[col] - colCount[col]):
        for r in range(len(board)):
            if board[r][col] == "?":
                board[r][col] = "X"
                colCount[col] += 1
                rowCount[r] += 1
                markAdjaToTent(r,col)
    if colTents[col] == colCount[col]:
        for r in range(len(board)):
            if board[r][col] == "?":
                board[r][col] = "."

import time
def main():
    readFile(sys.argv[1])
    printBoard()
    start = time.time()
    if solve():
        printBoard()
    print("execution time:"+str(time.time()-start))

if __name__ == "__main__":
    main()