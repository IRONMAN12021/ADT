import random

class TicTacToe:
    def __init__(self, difficulty='Easy', game_count=0):
        self.board = self.initialize_board()
        self.difficulty = difficulty
        self.game_count = game_count
        self.current_player = 'X' if game_count % 2 == 0 else 'O'  # Alternates starting player

    # Initialize the board
    def initialize_board(self):
        return [' ' for _ in range(9)]

    # Print the board
    def print_board(self):
        board = self.board
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("--|---|--")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("--|---|--")
        print(f"{board[6]} | {board[7]} | {board[8]}")

    # Check for a win
    def check_winner(self, player):
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]              # Diagonal
        ]
        for pattern in win_patterns:
            if all(self.board[i] == player for i in pattern):
                return True
        return False

    # Check for a draw
    def check_draw(self):
        return all(cell != ' ' for cell in self.board)

    # Get available moves
    def available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == ' ']

    # Easy AI move (random)
    def easy_ai_move(self):
        return random.choice(self.available_moves())

    # Medium AI move (block player's win)
    def medium_ai_move(self):
        for move in self.available_moves():
            self.board[move] = 'O'
            if self.check_winner('O'):
                self.board[move] = ' '
                return move
            self.board[move] = ' '
        for move in self.available_moves():
            self.board[move] = 'X'
            if self.check_winner('X'):
                self.board[move] = ' '
                return move
            self.board[move] = ' '
        return self.easy_ai_move()

    # Hard AI move (minimax algorithm)
    def minimax(self, depth, is_maximizing):
        if self.check_winner('O'):
            return 10 - depth
        if self.check_winner('X'):
            return depth - 10
        if self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in self.available_moves():
                self.board[move] = 'O'
                score = self.minimax(depth + 1, False)
                self.board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.board[move] = 'X'
                score = self.minimax(depth + 1, True)
                self.board[move] = ' '
                best_score = min(score, best_score)
            return best_score

    def hard_ai_move(self):
        best_move = None
        best_score = -float('inf')
        for move in self.available_moves():
            self.board[move] = 'O'
            score = self.minimax(0, False)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    # Get AI move based on difficulty
    def get_ai_move(self):
        if self.difficulty == 'Easy':
            return self.easy_ai_move()
        elif self.difficulty == 'Medium':
            return self.medium_ai_move()
        elif self.difficulty == 'Hard':
            return self.hard_ai_move()

    # Make a move
    def make_move(self, position, player):
        if self.board[position] == ' ':
            self.board[position] = player
            return True
        return False

    # Switch player
    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'


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
    game_count = 0
    difficulty = select_difficulty()

    while True:
        game = TicTacToe(difficulty, game_count)
        while True:
            game.print_board()

            if game.current_player == 'X':  # Human's turn
                move = int(input("Enter your move (1-9): ")) - 1
                if game.make_move(move, 'X'):
                    if game.check_winner('X'):
                        game.print_board()
                        print("Congratulations! You win!")
                        break
                    game.switch_player()
                else:
                    print("Invalid move. Try again.")
            else:  # AI's turn
                move = game.get_ai_move()
                game.make_move(move, 'O')
                if game.check_winner('O'):
                    game.print_board()
                    print("AI wins!")
                    break
                game.switch_player()

            if game.check_draw():
                game.print_board()
                print("It's a draw!")
                break

        game_count += 1
        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() != 'y':
            break

if __name__ == "__main__":
    play_game()
