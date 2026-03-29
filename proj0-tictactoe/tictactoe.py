"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# why does this take a board as input?  can there be more than one board in an instace?
# ah... it wants us to count the number of Xs vs Os on an input board to determine who's next
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cntX = 0
    cntO = 0

    for i in range(3):
        for j in range(3):
            if (board[i][j] == X):
                cntX = cntX + 1
            if (board[i][j] == O):
                cntO = cntO + 1

    # X always goes first, so initial state would be 0,0
    if (cntX > cntO):
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    out = set()

    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                out.add( (i,j) )

    return out

def deepCopyBoard(board):
    outboard = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]

    # deep copy board
    for i in range(3):
        for j in range(3):
            outboard[i][j] = board[i][j]

    return outboard

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if (board[action[0]][action[1]] != EMPTY):
        raise AssertionError("result(): cannot call action on cell that is already used")
    if (action[0] > 2 or 
        action[1] > 2 or
        action[0] < 0 or
        action[1] < 0):
        raise AssertionError("result(): out-of-bounds")

    outboard = deepCopyBoard(board)    

    # we need to know which player (X or O) is making the action.  Is action a struct?
    # or a global "current player"
    # result is called in runner.py:116 and 128, which passes in a tuple for action,
    # so I think we need a current player, but player takes a board as input
    # oh, we have a function to determine who's turn it is above
    outboard[action[0]][action[1]] = player(board)

    return outboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        if ((board[i][0] == board[i][1]) and (board[i][1] == board[i][2])):
            if (board[i][0] != EMPTY):
                return board[i][0]
        
    for j in range(3):
        if ((board[0][j] == board[1][j]) and (board[1][j] == board[2][j])):
            if (board[0][j] != EMPTY):
                return board[0][j]
    
    if ((board[0][0] == board[1][1]) and (board[1][1] == board[2][2])):
        if (board[1][1] != EMPTY):
            return board[1][1]
    if ((board[2][0] == board[1][1]) and (board[1][1] == board[0][2])):
        if (board[1][1] != EMPTY):
            return board[1][1]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) is not None):
        return True
    
    foundEmpty = False
    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                foundEmpty = True
                break
    
    if (foundEmpty):
        return False
    else:
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # assert that utliity() is only called if terminal() returns true

    w = winner(board)

    if (w == X):
        return 1
    elif (w == O):
        return -1
    else:
        return 0

def maxValue(board, bestAction):
    if (terminal(board)):
        return utility(board)
    
    v = -100
    for action in actions(board):
        x = max(v, minValue(result(board,action),bestAction))
        if (x > v): # this will find the first child that satisfies this condition (is this optimal? I can beat this algo)
            bestAction[0] = action
            v = x
            # short-circuit if we've hit the known max
            # for the first move, this short-circuit reduced time from 1.702119 seconds to 1.180767 seconds
            # if (v == 1):
            #    break

    return v

def minValue(board, bestAction):
    if (terminal(board)):
        return utility(board)
    
    v = 100 # supposed to be infinity (maxval, but we know our functions only return -1,0,1)
    for action in actions(board):
        x = min(v, maxValue(result(board,action),bestAction))
        if (x < v):
            bestAction[0] = action
            v = x
            # short-circuit if we've hit the known min
            #if (v == -1):
            #    break
    
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    - board input is the root of the minmax tree
    """
    if (terminal(board)):
        return None

    p = player(board)

    bestAction = [None]

    # X wants 1 (max), see utility()
    if (p == X): 
        maxValue(board, bestAction)
    else:
        minValue(board, bestAction)

    if (bestAction[0] == None):
        raise AssertionError
    
    return bestAction[0]


