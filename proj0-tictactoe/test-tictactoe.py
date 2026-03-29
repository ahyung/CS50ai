import csv
import sys
import time

from tictactoe import initial_state
from tictactoe import player
from tictactoe import actions
from tictactoe import result
from tictactoe import winner
from tictactoe import terminal
from tictactoe import minimax

def main():
    b = initial_state()
    dbgPrintBoard(b)
    b[0][0] = X
    dbgPrintBoard(b)
    b[0][1] = O
    dbgPrintBoard(b)

    #testWinner()
    #testResult()
    #testTerminal()

    #testminimax()

def printBoard(board):
    for i in range(3):
        print( board[i] )

def dbgPrintBoard(board):
    print ( "player turn: " + player(board) )
    print ( "actions:" )
    print ( actions(board) )
    printBoard(board)
    print ("\n")

X = "X"
O = "O"
EMPTY = None


def playerAlternating():
    """
    Returns player who has the next turn using global rule that X always goes first 
    (only works for one board)
    """
    if not hasattr(player, "turnX"):
        player.turnX = True  # Initialize once

    if (player.turnX):
        t = X
    else:
        t = O

    player.turnX = not player.turnX

    return t

def testResult():
    print("testResult")
    
    b = initial_state()
    printBoard(result(b,(0,0)))
    print("\n")
    printBoard(result(b,(1,1)))
    print("\n")
    printBoard(result(b,(2,2)))
    print("\n")

    b[1][1] = X
    printBoard(result(b,(0,0)))
    print("\n")
    try:
        printBoard(result(b,(1,1)))
    except AssertionError:
        print("assert: invalid action on result() call")
    print("\n")
    printBoard(result(b,(2,2)))
    print("\n")

def testWinner():
    print("testWinner")

    b = initial_state()
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")
    
    b = initial_state()
    b[0][0] = X
    b[0][1] = X
    b[0][2] = X
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")

    b = initial_state()
    b[1][0] = X
    b[1][1] = X
    b[1][2] = X
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")

    b = initial_state()
    b[2][0] = X
    b[2][1] = X
    b[2][2] = X
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")

    b = initial_state()
    b[0][0] = X
    b[1][0] = X
    b[2][0] = X
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")

    b = initial_state()
    b[0][1] = X
    b[1][1] = X
    b[2][1] = X
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")

    b = initial_state()
    b[0][2] = X
    b[1][2] = X
    b[2][2] = X
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")

    b = initial_state()
    b[0][0] = X
    b[1][1] = X
    b[2][2] = X
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")

    b = initial_state()
    b[0][2] = X
    b[1][1] = X
    b[2][0] = X
    printBoard(b)
    print("winner is ")
    print(winner(b))
    print("\n")

def testTerminal():
    print("testTerminal")

    b = initial_state()
    printBoard(b)
    print("terminal is ")
    print(terminal(b))

    b = initial_state()
    for i in range(3):
        for j in range(3):
            b[i][j] = X
    printBoard(b)
    print("terminal is ")
    print(terminal(b))

    b = initial_state()
    b[0][2] = X
    b[1][1] = X
    b[2][0] = X
    printBoard(b)
    print("terminal is ")
    print(terminal(b))

def testminimax():
    print ("testminimax")

    b = initial_state()
    printBoard(b)
    start = time.perf_counter()
    action = minimax(b)
    print( action )
    end = time.perf_counter()
    print(f"Execution time: {end - start:.6f} seconds")

    for i in range(8):
        if (i % 2 == 0):
            b[action[0]][action[1]] = X
        else:
            b[action[0]][action[1]] = O

        printBoard(b)
        start = time.perf_counter()
        action = minimax(b)
        print( action )
        end = time.perf_counter()
        print(f"Execution time: {end - start:.6f} seconds")

# needed this to designate a main to run... maybe python version?
if __name__ == "__main__":
    main()
