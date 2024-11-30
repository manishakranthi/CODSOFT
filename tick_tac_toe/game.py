from flask import Flask, render_template, request, redirect, url_for
import random
import ast  # For safely evaluating strings to list

app = Flask(__name__)

# Constants for the players
PLAYER_X = "X"  # Player
PLAYER_O = "O"  # AI
EMPTY = " "  # Empty cell

# Function to check for a win condition
def check_win(board, player):
    # Check rows, columns, and diagonals for a win
    for row in board:
        if row.count(player) == 3:
            return True
    for col in range(3):
        if [board[row][col] for row in range(3)].count(player) == 3:
            return True
    if [board[i][i] for i in range(3)].count(player) == 3:
        return True
    if [board[i][2-i] for i in range(3)].count(player) == 3:
        return True
    return False

# Function to check for a draw
def is_draw(board):
    return all(board[row][col] != EMPTY for row in range(3) for col in range(3))

# Minimax algorithm to choose the best move for AI
def minimax(board, depth, is_maximizing):
    if check_win(board, PLAYER_O):  # AI wins
        return 1
    if check_win(board, PLAYER_X):  # Player wins
        return -1
    if is_draw(board):  # Draw
        return 0

    if is_maximizing:  # Maximizing for AI
        best = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = EMPTY
        return best
    else:  # Minimizing for player
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = EMPTY
        return best

# AI's best move
def best_move(board):
    best_val = -float('inf')
    move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_O
                move_val = minimax(board, 0, False)
                board[i][j] = EMPTY
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

# Function to update the game board after player's turn
def player_turn(board, row, col):
    if board[row][col] == EMPTY:
        board[row][col] = PLAYER_X
    return board

# Function for AI's turn
def ai_turn(board):
    move = best_move(board)
    board[move[0]][move[1]] = PLAYER_O
    return board

@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize or load the board and game state
    if "board" not in request.cookies:
        board = [[EMPTY for _ in range(3)] for _ in range(3)]
        winner = None
        game_over = False
    else:
        # Load the game state from cookies (simplified example)
        board = ast.literal_eval(request.cookies.get("board"))
        winner = None
        game_over = False
    
    if request.method == "POST":
        # Handle player's move
        row = int(request.form["row"])
        col = int(request.form["col"])
        if board[row][col] == EMPTY:
            board = player_turn(board, row, col)
            if check_win(board, PLAYER_X):
                winner = "Player X"
                game_over = True
            elif is_draw(board):
                winner = "Draw"
                game_over = True
            else:
                # AI's turn
                board = ai_turn(board)
                if check_win(board, PLAYER_O):
                    winner = "AI O"
                    game_over = True
                elif is_draw(board):
                    winner = "Draw"
                    game_over = True

        # Save the updated board in cookies
        resp = redirect(url_for("home"))
        resp.set_cookie("board", str(board))
        return resp
    
    return render_template("index.html", board=board, winner=winner, game_over=game_over)

if __name__ == "__main__":
    app.run(debug=True)
