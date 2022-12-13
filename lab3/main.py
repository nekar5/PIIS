import chess
import time
import chess.engine as ce

engine = chess.engine.SimpleEngine.popen_uci(
    r"C:\Users\Nestor\Desktop\Files\3\piis\lab3\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")


def eval(board, maxTurn):
    info = engine.analyse(board, ce.Limit(depth=1))

    if ~maxTurn:
        result = ce.PovScore(info['score'], chess.BLACK).pov(
            chess.BLACK).relative.score()
    else:
        result = ce.PovScore(info['score'], chess.WHITE).pov(
            chess.WHITE).relative.score()

    if result == None:
        result = 0

    return result


def get_move_negaMax(board, depth):
    def negaMax(board, depth, is_max):
        if depth == 0:
            return eval(board, is_max)

        maxVal = -1_000_000

        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            copy = board.copy()
            copy.push(move)
            value = -negaMax(copy, depth - 1, 1 - is_max)

            if value > maxVal:
                maxVal = value

        return maxVal

    maxVal = -1_000_000
    best = None

    for legal_move in board.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        copy = board.copy()
        copy.push(move)
        value = -negaMax(copy, depth, 1 - copy.turn)

        if value > maxVal:
            maxVal = value
            best = move

    return best


def get_move_negaScout(board, depth, alpha=-999999, beta=999999):
    def negaScout(board, depthIn, alpha, beta):
        if depthIn == 0:
            return eval(board, board.turn)
        score = -1_000_000
        n = beta
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            copy = board.copy()
            copy.push(move)
            cur = -negaScout(copy, depthIn - 1, -n, -alpha)
            if cur > score:
                if n == beta or depthIn <= 2:
                    score = cur
                else:
                    scoreIn = -negaScout(copy, depthIn - 1, -beta, -cur)
            if score > alpha:
                alpha = score
            if alpha >= beta:
                return alpha
            n = alpha + 1
        return score

    score = -1_000_000
    best = None
    for legal_move in board.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        copy = board.copy()
        copy.push(move)
        value = -negaScout(copy, depth, alpha, beta)
        if value > score:
            score = value
            best = move

    return best


def get_move_pvs(board_instance, depth, alpha=-999999, beta=999999):
    def pvs(board, depthIn, alphaIn, betaIn):
        if depthIn == 0:
            return eval(board, board.turn)
        bSearch = True
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            copy = board.copy()
            copy.push(move)
            if bSearch:
                cur = -pvs(copy, depthIn - 1, -betaIn, -alphaIn)
            else:
                cur = -pvs(copy, depthIn - 1, -alphaIn - 1, -alphaIn)
                if alphaIn < cur < betaIn:
                    cur = -pvs(copy, depthIn - 1, -betaIn, -alphaIn)
            if cur >= betaIn:
                return betaIn
            if cur > alphaIn:
                alphaIn = cur
                bSearch = False

        return alphaIn

    score = -1_000_000
    best = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        copy = board_instance.copy()
        copy.push(move)
        value = -pvs(copy, depth, alpha, beta)
        if value > score:
            score = value
            best = move

    return best


def cvc_negaMax(depth=1):
    board = chess.Board()
    n = 0

    while (board.is_checkmate() != True and
           board.is_fivefold_repetition() != True and
           board.is_seventyfive_moves() != True):

        start = time.time()
        if n % 2 == 0:
            print("WHITE moves")
            move = get_move_negaMax(board, depth)
        else:
            print("BLACK moves")
            move = get_move_negaMax(board, depth)
        end = time.time()

        if move == None:
            print("game finished, checkmate")
            break

        print("move:", move, "\n"
              "time:", end - start, "\n"
              "move count:", n, "\n"
              "five fold", board.is_fivefold_repetition(), "\n")

        board.push(move)
        print(board, "\n")

        n += 1
    if board.is_fivefold_repetition():
        print("game finished, fivefold")


def cvc_negaScout(depth=1):
    board = chess.Board()
    n = 0

    while (board.is_checkmate() != True and
           board.is_fivefold_repetition() != True and
           board.is_seventyfive_moves() != True):

        start = time.time()
        if n % 2 == 0:
            print("WHITE moves")
            move = get_move_negaScout(board, depth)
        else:
            print("BLACK moves")
            move = get_move_negaScout(board, depth)
        end = time.time()

        if move == None:
            print("game finished, checkmate")
            break

        print("move:", move, "\n"
              "time:", end - start, "\n"
              "move count:", n, "\n"
              "five fold", board.is_fivefold_repetition(), "\n")

        board.push(move)
        print(board, "\n")

        n += 1
    if board.is_fivefold_repetition():
        print("game finished, fivefold")


def cvc_pvs(depth=1):
    board = chess.Board()
    n = 0

    while (board.is_checkmate() != True and
           board.is_fivefold_repetition() != True and
           board.is_seventyfive_moves() != True):

        start = time.time()
        if n % 2 == 0:
            print("WHITE moves")
            move = get_move_pvs(board, depth)
        else:
            print("BLACK moves")
            move = get_move_pvs(board, depth)
        end = time.time()

        if move == None:
            print("game finished, checkmate")
            break

        print("move:", move, "\n"
              "time:", end - start, "\n"
              "move count:", n, "\n"
              "five fold", board.is_fivefold_repetition(), "\n")

        board.push(move)
        print(board, "\n")

        n += 1
    if board.is_fivefold_repetition():
        print("game finished, fivefold")


if __name__ == '__main__':
    # cvc_negaMax()
    # cvc_negaScout()
    cvc_pvs()
    engine.quit()
