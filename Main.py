import random

# Initialize the board
def initialize_board():
    return [' ' for _ in range(9)]

# Print the board
def print_board(board):
    print("Current Board:")
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]}")

# Check for a win
def check_winner(board, player):
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for pattern in win_patterns:
        if all(board[i] == player for i in pattern):
            return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for cell in board)

# Get available moves
def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == ' ']

# Easy AI move (random)
def easy_ai_move(board):
    return random.choice(available_moves(board))

# Medium AI move (block player's win)
def medium_ai_move(board):
    for move in available_moves(board):
        board[move] = 'O'
        if check_winner(board, 'O'):
            board[move] = ' '
            return move
        board[move] = ' '
    for move in available_moves(board):
        board[move] = 'X'
        if check_winner(board, 'X'):
            board[move] = ' '
            return move
        board[move] = ' '
    return easy_ai_move(board)

# Hard AI move (minimax algorithm)
def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 10 - depth
    if check_winner(board, 'X'):
        return depth - 10
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for move in available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth + 1, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth + 1, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def hard_ai_move(board):
    best_move = None
    best_score = -float('inf')
    for move in available_moves(board):
        board[move] = 'O'
        score = minimax(board, 0, False)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

# Get AI move based on difficulty
def get_ai_move(board, difficulty):
    if difficulty == 'Easy':
        return easy_ai_move(board)
    elif difficulty == 'Medium':
        return medium_ai_move(board)
    elif difficulty == 'Hard':
        return hard_ai_move(board)

# Display home screen and select difficulty
def select_difficulty():
    print("Welcome to Tic-Tac-Toe!")
    print("Select difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    choice = input("Enter choice (1/2/3): ")
    if choice == '1':
        return 'Easy'
    elif choice == '2':
        return 'Medium'
    elif choice == '3':
        return 'Hard'
    else:
        print("Invalid choice, defaulting to Easy.")
        return 'Easy'

# Main game loop
def play_game():
    difficulty = select_difficulty()
    player_starts = True
    player_score = 0
    ai_score = 0

    while True:
        board = initialize_board()
        current_player = 'X' if player_starts else 'O'
        print(f"\n{'Player' if player_starts else 'AI'} starts the game!")

        while True:
            print_board(board)
            if current_player == 'X':  # Human's turn
                move = int(input("Enter your move (1-9): ")) - 1
                if board[move] == ' ':
                    board[move] = 'X'
                    if check_winner(board, 'X'):
                        print_board(board)
                        print("Congratulations! You win!")
                        player_score += 1
                        break
                    current_player = 'O'
                else:
                    print("Invalid move. Try again.")
            else:  # AI's turn
                move = get_ai_move(board, difficulty)
                board[move] = 'O'
                print("AI chose:", move + 1)
                if check_winner(board, 'O'):
                    print_board(board)
                    print("AI wins!")
                    ai_score += 1
                    break
                current_player = 'X'

            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

        print(f"Score: You {player_score} - AI {ai_score}")

        # Alternate who starts the game next
        player_starts = not player_starts

        # Option to restart or quit
        play_again = input("Play again? (y/n): ")
        if play_again.lower() != 'y':
            break

if __name__ == "__main__":
    play_game()
