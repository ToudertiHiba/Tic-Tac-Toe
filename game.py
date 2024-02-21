import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
MARGIN = 64
BOARD_LENGTH = 600
CELL_LENGTH = BOARD_LENGTH / 3
WIDTH, HEIGHT = BOARD_LENGTH + 2 * MARGIN , BOARD_LENGTH + 2 * MARGIN
BG_COLOR = (255, 240, 245)

# Load assets
FONT = pygame.font.Font("assets/Roboto-Regular.ttf", 100)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

BOARD = pygame.image.load("assets/Board.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")
WINNING_IMG = {winner: pygame.image.load(f"assets/Winning_{winner}.png") for winner in ['X', 'O']}

def reset_game():
    """Reset the game state."""
    global board, graphical_board, to_move, game_finished
    # Initialize board and graphical board
    board = [[None, None, None] for _ in range(3)]
    graphical_board = [[[None, None], [None, None], [None, None]], 
                       [[None, None], [None, None], [None, None]], 
                       [[None, None], [None, None], [None, None]]]
    to_move = 'X'
    # Clear the screen and display the initial board
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (MARGIN, MARGIN))
    game_finished = False
    pygame.display.update()

# Initialize game state
reset_game()

def render_board():
    """Render X and O on the board."""
    global board, graphical_board
    for i in range(3):
        for j in range(3):
            center =  (j*CELL_LENGTH + CELL_LENGTH/2 + MARGIN, i*CELL_LENGTH + CELL_LENGTH/2 + MARGIN)
            img_dictionary = {"X": X_IMG, "O": O_IMG}
            if board[i][j] in img_dictionary:
                img = img_dictionary[board[i][j]]
                graphical_board[i][j][0] = img # Surface (image)
                graphical_board[i][j][1] = img.get_rect(center = center) # Rectangle 
    
def add_XO():
    """Add X or O to the board based on mouse click."""
    global board, graphical_board, to_move
    current_pos = pygame.mouse.get_pos()
    x, y = current_pos
    converted_x = math.floor((x - 64)/CELL_LENGTH)
    converted_y = math.floor((y - 64)/CELL_LENGTH)
    if 0 <= converted_x <= 2 and 0 <= converted_y <= 2:
        if board[converted_y][converted_x] is None:
            board[converted_y][converted_x] = to_move
            to_move = 'O' if to_move == 'X' else 'X'  # Switch player
    render_board()
    for i in  range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])

def check_win():
    """
    Check if there is a winner or if the game ended in a draw.

    Returns:
        str or None: 'X' if player X wins, 'O' if player O wins, 'DRAW' if the game ends in a draw,
                     None if the game is still ongoing.
    """
    global board, graphical_board
    
    # Check rows for a win
    for row in range(3):
        if((board[row][0] == board[row][1] == board[row][2]) and (board [row][0] is not None)):            
            # Update graphical board with winning images
            winner = board[row][0]
            for i in range(3):
                graphical_board[row][i][0] = WINNING_IMG[winner]
                SCREEN.blit(graphical_board[row][i][0], graphical_board[row][i][1])
            pygame.display.update()
            return winner

    # Check columns for a win
    for col in range(3):
        if((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):            
            # Update graphical board with winning images
            winner =  board[0][col]
            for i in range(3):
                graphical_board[i][col][0] = WINNING_IMG[winner]
                SCREEN.blit(graphical_board[i][col][0], graphical_board[i][col][1])
            pygame.display.update()
            return winner
    
    # Check diagonal (top-left to bottom-right) for a win
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # Update graphical board with winning images
        winner =  board[0][0]
        for i in range(3):
            graphical_board[i][i][0] = WINNING_IMG[winner]
            SCREEN.blit(graphical_board[i][i][0], graphical_board[i][i][1])
        pygame.display.update()
        return winner
    
    # Check diagonal (top-right to bottom-left) for a win
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # Update graphical board with winning images
        winner =  board[0][2]
        for i in range(3):
            graphical_board[i][2-i][0] = WINNING_IMG[winner]
            SCREEN.blit(graphical_board[i][2-i][0], graphical_board[i][2-i][1])
        pygame.display.update()
        return winner
    
    # Check for a draw
    for i in range(3):
        for j in range(3):
            if board[i][j] not in ['X', 'O']:
                return None  # Game still ongoing
    return "DRAW"  # Game ended in a draw

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            add_XO()
            if game_finished:
                reset_game()                
            if check_win() is not None:
                game_finished = True
            pygame.display.update()