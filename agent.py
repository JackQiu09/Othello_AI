"""
An AI player for Othello.
"""
import math
import random
import sys
import time
from heapq import heappush, heappop

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

caching_states = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    p1, p2 = get_score(board)
    if color == 1:
        return p1 - p2
    return p2 - p1


# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    if color == 1:
        opp = 2
    else:
        opp = 1

    p1, p2 = get_score(board)
    diff = p1 - p2
    diff2 = p2 - p1

    max_corner = 0
    min_corner = 0
    n = len(board)
    corner_list = [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]
    for c in corner_list:
        if board[c[0]][c[1]] == color:
            max_corner += 1
        if board[c[0]][c[1]] == opp:
            min_corner += 1
    if (max_corner + min_corner) != 0:
        heur = 100 * (max_corner - min_corner) / (max_corner + min_corner)
    else:
        heur = 0
    if heur != 0:
        return heur
    else:
        if color == 1:
            return diff
        return diff2


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    if color == 1:
        min_p = 2
    else:
        min_p = 1

    best_move = None
    moves = get_possible_moves(board, min_p)
    value = math.inf

    if not moves or limit == 0:
        return best_move, compute_utility(board, color)
    for m in moves:
        b = play_move(board, min_p, m[0], m[1])
        if caching == 1:
            if b in caching_states:
                nxt_val = caching_states[b]
                if value > nxt_val:
                    best_move, value = m, nxt_val
            else:
                if limit > 0:
                    nxt_move, nxt_val = minimax_max_node(b, color, limit - 1,
                                                           caching)
                    if value > nxt_val:
                        best_move, value = m, nxt_val
                    caching_states[b] = value
                else:
                    nxt_move, nxt_val = minimax_max_node(b, color, limit,
                                                           caching)
                    if value > nxt_val:
                        best_move, value = m, nxt_val
                    caching_states[b] = value
                    best_move = m
        else:
            if limit > 0:
                nxt_move, nxt_val = minimax_max_node(b, color, limit - 1,
                                                       caching)
            else:
                nxt_move, nxt_val = minimax_max_node(b, color, limit, caching)
            if value > nxt_val:
                best_move, value = m, nxt_val
    return best_move, value


def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    best_move = None
    moves = get_possible_moves(board, color)
    value = -math.inf

    if not moves or limit == 0:
        return best_move, compute_utility(board, color)
    for m in moves:
        b = play_move(board, color, m[0], m[1])
        if caching == 1:
            if b in caching_states:
                nxt_val = caching_states[b]
                if value < nxt_val:
                    best_move, value = m, nxt_val
            else:
                if limit > 0:
                    nxt_move, nxt_val = minimax_min_node(b, color, limit - 1,
                                                           caching)
                    if value < nxt_val:
                        best_move, value = m, nxt_val
                    caching_states[b] = value
                else:
                    nxt_move, nxt_val = minimax_min_node(b, color, limit,
                                                           caching)
                    if value < nxt_val:
                        best_move, value = m, nxt_val
                    caching_states[b] = value
        else:
            if limit > 0:
                nxt_move, nxt_val = minimax_min_node(b, color, limit - 1,
                                                       caching)
            else:
                nxt_move, nxt_val = minimax_min_node(b, color, limit, caching)
            if value < nxt_val:
                best_move, value = m, nxt_val
    return best_move, value


def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    best_move = None
    moves = get_possible_moves(board, color)
    value = -math.inf

    if not moves:
        return best_move

    for m in moves:
        b = play_move(board, color, m[0], m[1])
        if caching == 1:
            if b in caching_states:
                nxt_val = caching_states[b]
            else:
                if limit > 0:
                    nxt_move, nxt_val = minimax_min_node(b, color, limit - 1, caching)
                    caching_states[b] = nxt_val
                else:
                    nxt_move, nxt_val = minimax_min_node(b, color, limit, caching)
                    caching_states[b] = nxt_val
        else:
            if limit > 0:
                nxt_move, nxt_val = minimax_min_node(b, color, limit - 1, caching)
            else:
                nxt_move, nxt_val = minimax_min_node(b, color, limit, caching)
        if value < nxt_val:
            best_move, value = m, nxt_val
    return best_move


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if color == 1:
        min_p = 2
    else:
        min_p = 1

    best_move = None
    moves = get_possible_moves(board, min_p)
    value = math.inf

    if not moves or limit == 0:
        return best_move, compute_utility(board, color)
    states_list = []
    states = []
    move = []
    for m in moves:
        b = play_move(board, min_p, m[0], m[1])
        if ordering == 1:
            utl = compute_utility(b, color)
            heappush(states_list, (utl, b, m))
        else:
            states.append(b)
            move.append(m)
    if ordering == 1:
        while states_list:
            s = heappop(states_list)
            states.append(s[1])
            move.append(s[2])
    for i in range(len(states)):
        if caching == 1:
            if states[i] in caching_states:
                nxt_val = caching_states[states[i]]
                if value > nxt_val:
                    best_move, value = move[i], nxt_val
            else:
                if limit > 0:
                    nxt_move, nxt_val = alphabeta_max_node(states[i], color,
                                                           alpha, beta,
                                                           limit - 1,
                                                           caching)
                    if value > nxt_val:
                        best_move, value = move[i], nxt_val
                    caching_states[states[i]] = value
                else:
                    nxt_move, nxt_val = alphabeta_max_node(states[i], color,
                                                           alpha, beta,
                                                           limit, caching)
                    if value > nxt_val:
                        best_move, value = move[i], nxt_val
                    caching_states[states[i]] = value
        else:
            if limit > 0:
                nxt_move, nxt_val = alphabeta_max_node(states[i], color,
                                                       alpha, beta,
                                                       limit - 1, caching)
            else:
                nxt_move, nxt_val = alphabeta_max_node(states[i], color,
                                                       alpha, beta, limit,
                                                       caching)
            if value > nxt_val:
                best_move, value = move[i], nxt_val
        if value <= alpha:
            return best_move, value
        beta = min(beta, value)
    return best_move, value


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    best_move = None
    moves = get_possible_moves(board, color)
    value = -math.inf

    if not moves or limit == 0:
        return best_move, compute_utility(board, color)
    states_list = []
    states = []
    move = []
    for m in moves:
        b = play_move(board, color, m[0], m[1])
        if ordering == 1:
            utl = compute_utility(b, color)
            heappush(states_list, (-utl, b, m))
        else:
            states.append(b)
            move.append(m)
    if ordering == 1:
        while states_list:
            s = heappop(states_list)
            states.append(s[1])
            move.append(s[2])
    for i in range(len(states)):
        if caching == 1:
            if states[i] in caching_states:
                nxt_val = caching_states[states[i]]
                if value < nxt_val:
                    best_move, value = move[i], nxt_val
            else:
                if limit > 0:
                    nxt_move, nxt_val = alphabeta_min_node(states[i], color,
                                                           alpha, beta,
                                                           limit - 1,
                                                           caching)
                    if value < nxt_val:
                        best_move, value = move[i], nxt_val
                    caching_states[states[i]] = value
                else:
                    nxt_move, nxt_val = alphabeta_min_node(states[i], color,
                                                           alpha, beta,
                                                           limit, caching)
                    if value < nxt_val:
                        best_move, value = move[i], nxt_val
                    caching_states[states[i]] = value
        else:
            if limit > 0:
                nxt_move, nxt_val = alphabeta_min_node(states[i], color,
                                                       alpha, beta,
                                                       limit - 1, caching)
            else:
                nxt_move, nxt_val = alphabeta_min_node(states[i], color,
                                                       alpha, beta, limit,
                                                       caching)

            if value < nxt_val:
                best_move, value = move[i], nxt_val
        if value >= beta:
            return best_move, value
        alpha = max(alpha, value)
    return best_move, value


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    value = -math.inf
    beta = math.inf
    best_move = None
    moves = get_possible_moves(board, color)

    if not moves:
        return best_move
    states_list = []
    states = []
    move = []
    for m in moves:
        b = play_move(board, color, m[0], m[1])
        if ordering == 1:
            utl = compute_utility(b, color)
            heappush(states_list, (-utl, b, m))
        else:
            states.append(b)
            move.append(m)
    if ordering == 1:
        while states_list:
            s = heappop(states_list)
            states.append(s[1])
            move.append(s[2])
    for i in range(len(states)):
        if caching == 1:
            if states[i] in caching_states:
                nxt_val = caching_states[states[i]]
            else:
                if limit > 0:
                    nxt_move, nxt_val = alphabeta_min_node(states[i], color,
                                                           value, beta,
                                                           limit - 1,
                                                           caching)
                    caching_states[states[i]] = nxt_val
                else:
                    nxt_move, nxt_val = alphabeta_min_node(states[i], color,
                                                           value, beta,
                                                           limit, caching)
                    caching_states[states[i]] = nxt_val
        else:
            if limit > 0:
                nxt_move, nxt_val = alphabeta_min_node(states[i], color,
                                                       value, beta,
                                                       limit - 1, caching)
            else:
                nxt_move, nxt_val = alphabeta_min_node(states[i], color,
                                                       value, beta, limit,
                                                       caching)
        if value < nxt_val:
            best_move, value = move[i], nxt_val
    return best_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Terminator") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print("FINAL {} {}".format(dark_score, light_score))
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
