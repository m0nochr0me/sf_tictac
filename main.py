"""
Tic Tac Toe (SF)

Available commands:
  [h]elp - print this help
  [n]ew (X|O) - start new game
  [r]reset - reset scores
  [m]ove N - place mark at N tile
  [d]ifficulty [1...4] - set difficulty (default 1)

  Ctrl+C to exit.
"""

import sys
from copy import deepcopy
from random import randint, choice


def cls():
    """Clear screen by printing newline a hundred times"""

    print('\n' * 100)


def check_win(board, mark='X'):
    """This abomination returns True if any win condition is satisfied for given mark"""

    # check every tile in every row
    # check every tile in every column
    # check tiles on forward diagonal
    # check files on backward diagonal
    return any(mark in b and b[:-1] == b[1:] for b in board) or \
        any(all(mark in b[i] and b[i][:-1] == b[i][1:] for b in board) for i in range(3)) or \
        all(mark in b and b[:-1] == b[1:] for b in [board[i][i] for i in range(3)]) or \
        all(mark in b and b[:-1] == b[1:] for b in [board[i][-(i-2)] for i in range(3)])


def mark_tile(board, tile, mark='X'):
    """Place mark on requested tile"""

    # Convert tile number into x/y coordinates
    x = (tile - 1) // 3
    y = (tile - 1) % 3
    if board[x][y] in 'XO':
        # Raising error making this def suitable for AI without additional checks
        raise ValueError('Tile already marked')
    else:
        board[x][y] = mark
    return board


def ai(board, mark='O', difficulty=1):
    """The [in]famous Artificial Intelligence"""

    possible_tiles = []  # all possible tiles
    counter_tiles = []  # tiles to counter human winning
    winning_tiles = []  # tiles leading to instant AI win
    for i in range(1, 10):
        # copy current board twice -_-
        # sometimes I think it wasn't good idea to use matrix for board
        # but now it's too late.
        new_board = deepcopy(board)
        counter_board = deepcopy(board)
        try:
            # check all possible, possible winning, and possible counter tiles
            new_board = mark_tile(new_board, i, mark)
            counter_board = mark_tile(counter_board, i, 'X' if mark == 'O' else 'O')
        except ValueError:
            continue
        else:
            # populate corresponding lists
            possible_tiles.append(i)
            if check_win(counter_board, 'X' if mark == 'O' else 'O'):
                counter_tiles.append(i)
            if check_win(new_board, mark):
                winning_tiles.append(i)

    # difficulty here is leaving space for AI to make errors so human can win
    # always prefer wining tiles
    if len(winning_tiles) > 0 and randint(1, 4) <= difficulty:
        return mark_tile(board, winning_tiles[0], mark)
    # if AI can't win, check if it can prevent human winning
    elif len(counter_tiles) > 0 and randint(1, 4) <= difficulty:
        return mark_tile(board, counter_tiles[0], mark)
    # mark random tiles if none of the above
    else:
        return mark_tile(board, choice(possible_tiles), mark)


def print_board(board, human_score=0, ai_score=0, difficulty=0):
    """Prints board and scores"""

    print(f'Human: {human_score} | AI: {ai_score} \nDifficulty: {difficulty}')
    for row in board:
        print('|' + '|'.join(row) + '|')


def get_cmd(mark='?'):
    """Reads command from standard input, and returns tuple with command and it's argument[s]"""

    try:
        cmd = input(f'?{mark}>')
        cmd_split = cmd.split()
    except KeyboardInterrupt:
        print('Ok Bye!')
        sys.exit(0)
    else:
        # always tuple for empty command to get rid of additional checks
        return cmd_split or ('x',)


def reset_board():
    """Returns default board with subscripted tiles"""

    return [['₁', '₂', '₃'], ['₄', '₅', '₆'], ['₇', '₈', '₉']]


def main():
    """Game controller"""

    # 0 - uninitialized
    # 1 - player's turn
    # 2 - ai's turn
    # 3 - game over
    game_state = 0
    human_score = ai_score = 0
    board = reset_board()
    player_mark = 'X'
    turn = 0
    difficulty = 1

    while True:
        if not game_state:
            print(__doc__)
            game_state = 1
            # actually game starts here

        cmd = get_cmd(player_mark)

        cls()
        # using startswith so it is unnecessary to type full command
        if cmd[0].startswith('n'):
            # New game
            board = reset_board()
            game_state = 1
            turn = 0
            # set human mark to X or O
            if len(cmd) > 1 and cmd[1] in 'XO':
                player_mark = cmd[1]
        elif cmd[0].startswith('d'):
            # Set difficulty
            if len(cmd) > 1 and cmd[1] in '1234':
                difficulty = int(cmd[1])
        elif cmd[0].startswith('m'):
            # Mark tile
            if game_state == 3:
                print('This game is finished.\nPlease start new game.')
                continue
            if len(cmd) > 1 and cmd[1] in '123456789':
                try:
                    # if tile can be marked, mark it, and give turn to ai
                    board = mark_tile(board, int(cmd[1]), player_mark)
                    turn += 1
                    game_state = 2
                except ValueError as e:
                    print(e)
                else:
                    if check_win(board, player_mark):
                        game_state = 3
                        human_score += 1
                        print('Human win')
            else:
                print('Invalid tile!')
        elif cmd[0].startswith('r'):
            # Reset scores
            human_score = ai_score = 0
        else:
            print('Unknown command!')

        if turn >= 9 and game_state != 3:
            # If there is no winner until ninth turn consider game a draw
            game_state = 3
            print('Draw')

        if game_state == 2:
            # AI's turn
            ai_mark = 'O' if player_mark == 'X' else 'X'
            board = ai(board, ai_mark, difficulty)
            game_state = 1
            turn += 1
            if check_win(board, ai_mark):
                game_state = 3
                ai_score += 1
                print('AI win')

        print_board(board, human_score, ai_score, difficulty)


main()
