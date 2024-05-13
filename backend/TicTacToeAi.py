import copy
import random

player, opponent = 'x', 'o'
DEPTH = 1


def rowOpp(board, size, player, opponent):
    row_score = 0
    for i in range(size):
        isBlocked = False
        count = 0
        for j in range(size):
            if board[i][j] == player:
                count += 1
            elif board[i][j] == opponent:
                isBlocked = True
        if isBlocked:
            row_score += 0
        else:
            row_score += count * (1.6 ** (count / 2) if count < size else 10)
    return row_score


def colOpp(board, size, player, opponent):
    col_score = 0
    for i in range(size):
        isBlocked = False
        count = 0
        for j in range(size):
            if board[j][i] == player:
                count += 1
            elif board[j][i] == opponent:
                isBlocked = True
        if isBlocked:
            col_score += 0
        else:
            col_score += count * (1.6 ** (count / 2) if count < size else 10)
    return col_score


def diagOpp(board, size, player, opponent):
    diag_score = 0
    count = 0
    isBlocked = False
    for i in range(size):
        if board[i][i] == player:
            count += 1
        elif board[i][i] == opponent:
            isBlocked = True
    if not isBlocked:
        diag_score += count * (1.6 ** (count / 2) if count < size else 10)

    count = 0
    isBlocked = False
    for i in range(size):
        if board[i][size - i - 1] == player:
            count += 1
        elif board[i][i] == opponent:
            isBlocked = True
    if not isBlocked:
        diag_score += count * (1.6 ** (count / 2) if count < size else 10)
    return diag_score


def opportunities(board, size):
    return (rowOpp(board, size, player=player, opponent=opponent)
            + colOpp(board, size, player=player, opponent=opponent)
            + diagOpp(board, size, player=player, opponent=opponent))


def threat(board, size):
    return - (rowOpp(board, size, player=opponent, opponent=player)
              + colOpp(board, size, player=opponent, opponent=player)
              + diagOpp(board, size, player=opponent, opponent=player))


def centerControl(board, size):
    return 10 if board[size//2][size//2] == player else -10


def evaluate(board, size):
    return opportunities(board, size) + threat(board, size) + centerControl(board, size)


def isTerminated(board, size):
    for i in range(size):
        # Check rows
        if board[i] == [player] * size:
            return True
        elif board[i] == [opponent] * size:
            return True
        # Check columns
        if all(row[i] == player for row in board):
            return True
        elif all(row[i] == opponent for row in board):
            return True
        # Check diagonals
    if board[0][0] != ' ' and all(board[i][i] == board[0][0] for i in range(size)):
        return True
    if board[0][size - 1] != ' ' and all(board[i][size - i - 1] == board[0][size - 1] for i in range(size)):
        return True
    return False


def minimax(board, size, role, depth, alpha, beta):
    if depth == DEPTH or isTerminated(board, size):
        return (0, 0), evaluate(board, size)
    else:
        move, score = (1, 1), -1e9
        score = 1e9 if role == 'opponent' else -1e9
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ' and role == 'player':
                    board[i][j] = player
                    _, new_score = minimax(board, size, 'opponent', depth + 1, alpha, beta)
                    if new_score >= score:
                        score = new_score
                        move = (i, j)
                        alpha = score
                        if alpha >= beta:
                            board[i][j] = ' '
                            return move, score
                    board[i][j] = ' '

                elif board[i][j] == ' ' and role == 'opponent':
                    board[i][j] = opponent
                    _, new_score = minimax(board, size, 'player', depth + 1, alpha, beta)
                    if new_score <= score:
                        score = new_score
                        move = (i, j)
                        beta = score
                        if alpha >= beta:
                            board[i][j] = ' '
                            return move, score
                    board[i][j] = ' '
        return move, score


def get_move(board, size):
    # if board[size // 2][size // 2] == ' ':
    #     return size // 2, size // 2
    move, score = minimax(board, size, 'player', 0, alpha=-1e9, beta=1e9)
    # print(board)
    return move


def get_rand_move(board, size):
    # Find all available positions on the board
    size = int(size)
    available_moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                available_moves.append((i, j))

    # If there are no available moves, return None
    if not available_moves:
        return None
    # Choose a random available move
    return available_moves[random.randint(0, len(available_moves) - 1)]


if __name__ == "__main__":
    a = [[' ', 'o', ' ', ' ', ' '],
         [' ', 'o', ' ', 'x', ' '],
         [' ', 'o', 'x', ' ', ' '],
         [' ', ' ', ' ', ' ', ' '],
         [' ', 'o', 'x', ' ', ' ']]
    # print(rowOpp(a, 5, player, opponent))
    # print(opportunities(a, 5))
    print(evaluate(a, 5))
