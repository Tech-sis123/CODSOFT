import math
import random

class TicTacToeGame:
    """Main game class that handles the board and game rules"""
    
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None  
        
    def show_board(self):
        """Display the current board state"""
        print("\nCurrent Board:")
        for i in range(3):
            row = self.board[i*3 : (i+1)*3]
            print("| " + " | ".join(row) + " |")
        print()
    
    @staticmethod
    def show_numbered_board():
        """Show which numbers correspond to which positions"""
        print("\nBoard Positions:")
        for i in range(3):
            row_numbers = [str(i*3 + j) for j in range(3)]
            print("| " + " | ".join(row_numbers) + " |")
        print()
    
    def available_moves(self):
        """Return list of empty squares (indices 0-8)"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def make_move(self, position, player_symbol):
        """Place a player's symbol on the board if move is valid"""
        if self.board[position] == ' ':
            self.board[position] = player_symbol
            if self.check_win(position, player_symbol):
                self.current_winner = player_symbol
            return True
        return False
    
    def check_win(self, position, player_symbol):
        """Check if the last move resulted in a win"""
        
        row_index = position // 3
        row = self.board[row_index*3 : (row_index + 1)*3]
        if all(spot == player_symbol for spot in row):
            return True
        
        
        col_index = position % 3
        column = [self.board[col_index + i*3] for i in range(3)]
        if all(spot == player_symbol for spot in column):
            return True
        
        
        if position % 2 == 0:  
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all(spot == player_symbol for spot in diagonal1):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all(spot == player_symbol for spot in diagonal2):
                return True
        
        return False
    
    def is_tie(self):
        """Check if the game is a tie (no winner and no moves left)"""
        return ' ' not in self.board and self.current_winner is None


class HumanPlayer:
    """Class to handle human player moves"""
    
    def __init__(self, symbol):
        self.symbol = symbol
    
    def get_move(self, game):
        """Get valid move input from human player"""
        while True:
            try:
                move = input(f"Your turn ({self.symbol}). Enter position (0-8): ")
                move = int(move)
                if move not in game.available_moves():
                    print("That position is already taken or invalid. Try again.")
                    continue
                return move
            except ValueError:
                print("Please enter a number between 0-8.")


class AIPlayer:
    """Class for the AI player using Minimax algorithm"""
    
    def __init__(self, symbol):
        self.symbol = symbol
    
    def get_move(self, game):
        """Determine the best move using Minimax"""
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())
        
        
        best_move = self.minimax(game, self.symbol)['position']
        return best_move
    
    def minimax(self, game, current_player, alpha=-math.inf, beta=math.inf):
        """Minimax algorithm with Alpha-Beta pruning"""
        if game.current_winner == self.symbol:
            return {'position': None, 'score': 1 * (game.num_empty_squares() + 1)}
        elif game.current_winner is not None:  
            return {'position': None, 'score': -1 * (game.num_empty_squares() + 1)}
        elif not game.available_moves():  
            return {'position': None, 'score': 0}
        
        
        if current_player == self.symbol:
            best = {'position': None, 'score': -math.inf}  
        else:
            best = {'position': None, 'score': math.inf} 
        
        
        for possible_move in game.available_moves():
            game.make_move(possible_move, current_player)
            
            
            simulated_score = self.minimax(
                game, 
                'O' if current_player == 'X' else 'X', 
                alpha, 
                beta
            )
            
            
            game.board[possible_move] = ' '
            game.current_winner = None
            simulated_score['position'] = possible_move
            
            
            if current_player == self.symbol:  
                if simulated_score['score'] > best['score']:
                    best = simulated_score
                alpha = max(alpha, best['score'])
            else:  
                if simulated_score['score'] < best['score']:
                    best = simulated_score
                beta = min(beta, best['score'])
            
            
            if alpha >= beta:
                break
        
        return best


def play_game():
    """Main function to play the game"""
    print("\nWelcome to Tic-Tac-Toe against an unbeatable AI!")
    print("You'll be X and the AI will be O.")
    print("Here's how the board positions are numbered:")
    

    game = TicTacToeGame()
    game.show_numbered_board()
    
    human = HumanPlayer('X')
    ai = AIPlayer('O')
    
    current_player = human  
    
    while True:
        game.show_board()
        
        
        if current_player == human:
            move = human.get_move(game)
        else:
            print("AI is thinking...")
            move = ai.get_move(game)
            print(f"AI chooses position {move}")
        
        game.make_move(move, current_player.symbol)
        
        
        if game.current_winner:
            game.show_board()
            print(f"{game.current_winner} wins!")
            break
        elif game.is_tie():
            game.show_board()
            print("It's a tie!")
            break
        
        
        current_player = ai if current_player == human else human
    

    play_again = input("\nPlay again? (y/n): ").lower()
    if play_again == 'y':
        play_game()
    else:
        print("Thanks for playing!")



def num_empty_squares(self):
    return len(self.available_moves())

TicTacToeGame.num_empty_squares = num_empty_squares

if __name__ == "__main__":
    play_game()
