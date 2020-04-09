# 1. setup an empty board
# 2. ask player to input where they would like to play their movie
# 3. check if the winning condition exists on the board, if so end game and announce winner else continue
# 4. repeat if no winner is found, repeat until winner is found

# board layout
#   1 2 3
# A 0 0 0
# B 0 0 0
# C 0 0 0

import pprint, time, os

# creates the initial board, returns a 2d array
def drawBoard():
    board = [["#" for cols in range(3)] for rows in range(3)]
    return board

# applies the players move and updates the board
def playerMove(playerSymbol, location, board):
    locations = {"A":0, "B":1, "C":2}
    if len(location) == 2 and location[0] in locations and int(location[1]) in [1, 2, 3]:
        position = [locations[location[0]], int(location[1]) - 1]
        if board[position[0]][position[1]] == "#":
            board[position[0]][position[1]] = playerSymbol
            return board
        else:
            return -1
    else:
        return -1

# checks the board to see if someone has won
def checkBoard(board):
    result1 = checkHor(board)
    result2 = checkCols(board)
    result3 = checkRows(board)
    result4 = checkFull(board)
    if (result1 != -1 or result2 != -1 or result3 != -1):
        return False
    elif result4:
        return False
    else:
        return True

# functions to check the board
def checkHor(board):
    if board[0][0] == board[1][1] == board[2][2] and not (board[0][0] == "#" or board[1][1] == "#" or board[2][2] == "#"):
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and not (board[0][2] == "#" or board[1][1] == "#" or board[0][2] == "#"):
        return board[0][2]
    return -1

def checkCols(board):
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and not (board[0][i] == "#" or board[1][i] == "#" or board[2][i] == "#"):
            return board[0][i]
    return -1

def checkRows(board):
    for i in board:
        if i == [i[0]] * 3 and not (i[0] == "#" or i[1] == "#" or i[2] == "#"):
            return i[0]
    return -1

def checkFull(board):
    for rows in range(3):
        for cols in range(3):
            if board[rows][cols] == "#":
                return False
    return True

# main loop for the game
def game():
    board, players, playing = drawBoard(), {1: {'symbol':'X'}, 2: {'symbol':'O'}}, True
    current_player = True # true for player 1, false for player 2
    while playing:
        os.system('clear')
        print("  1 2 3")
        print("A {}\nB {}\nC {}".format(" ".join(board[0]), " ".join(board[1]), " ".join(board[2])))
        print("Player {} your move. Enter a location A1-A3, B1-B3, C1-C3.\nType exit to quit the game.".format(1 if current_player else 2))
        location = input(">> ")
        if location.lower() != "exit":
            temp = playerMove(players[1 if current_player else 2]['symbol'], location.upper(), board)
        else:
            print("Quiting game.")
            break
        if temp != -1:
            board = temp
            check = checkBoard(board)
            if not check:
                playing = False
                os.system('clear')
                print("{}\n{}\n{}".format(" ".join(board[0]), " ".join(board[1]), " ".join(board[2])))
                if not checkFull(board):
                    print("Player {} has won the game.".format(1 if current_player else 2))
                else:
                    print("No-one won. Board is full.")
            current_player = not current_player
        else:
            print("Invalid, input please enter in the format A1-A3, B1-B3, C1-C3.\nAlso ensure that spot isn't taken.")
        time.sleep(0.2)
game()
