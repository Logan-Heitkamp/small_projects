import pygame

window_size = (720, 720)

screen = pygame.display.set_mode(window_size)

board_width = 7
board_height = 6

cell_size = 100

board_color = (0, 0, 255)
player_1_color = (255, 0, 0)
player_2_color = (255, 255, 0)
player_1_shadow = (226, 128, 131)
player_2_shadow = (237, 230, 179)
empty_color = 'grey'

pygame.display.set_caption("Connect Four")

main_board = [[0] * board_height for _ in range(board_width)]


# draws the current state of the board after every move
def draw_board(this_screen, board: list, winner: str) -> None:
    # draw board and background
    this_screen.fill((100, 100, 100))
    fill_screen(this_screen)

    # draw pieces or blank spots
    draw_circles(board, this_screen)

    if winner != '':

        # cleans up remaining shadow
        for idx_x, x in enumerate(main_board):
            for idx_y, y in enumerate(x):
                if y == 3 or y == 4:
                    main_board[idx_x][idx_y] = 0

        # creates the win text
        font = pygame.font.Font('freesansbold.ttf', 64)
        text = font.render(f'{winner} has won!', True, f'{winner}', (200, 200, 200))
        text_rect = text.get_rect()
        text_rect.center = (720 // 2, 55)
        this_screen.blit(text, text_rect)
        # pygame.draw.rect(screen, 'white', pygame.Rect(720 // 2 - 250, 720 // 2 - 150, 500, 300))

    # flips screen in order to see what was drawn
    pygame.display.flip()


def draw_circles(board, this_screen):
    for y in range(6):
        for x in range(7):
            if board[x][y] == 1:
                pygame.draw.circle(this_screen, player_1_color, (x * 100 + 60, 720 - (y * 100 + 60)), 40)
            elif board[x][y] == 2:
                pygame.draw.circle(this_screen, player_2_color, (x * 100 + 60, 720 - (y * 100 + 60)), 40)
            elif board[x][y] == 3:
                pygame.draw.circle(this_screen, player_1_shadow, (x * 100 + 60, 720 - (y * 100 + 60)), 40)
            elif board[x][y] == 4:
                pygame.draw.circle(this_screen, player_2_shadow, (x * 100 + 60, 720 - (y * 100 + 60)), 40)
            else:
                pygame.draw.circle(this_screen, empty_color, (x * 100 + 60, 720 - (y * 100 + 60)), 40)


def fill_screen(this_screen):
    pygame.Surface.fill(this_screen, 'blue',
                        pygame.Rect(window_size[0] // 2 - 350, window_size[1] // 2 - 250, 700, 600))


# places the pieces on main_board as the players make a move
# returns True if the piece could be placed, else returns False
def place_piece(board: list, column: int, current_player: int) -> bool:
    for idx, y in enumerate(board[column]):
        if y == 0 or y == 3 or y == 4:
            board[column][idx] = current_player
            return True
    return False


# places shadow in the column the mouse is currently in to indicate where a piece will be placed
def place_shadow(column, current_player) -> None:
    # removes all existing shadows
    for idx_x, x in enumerate(main_board):
        for idx_y, y in enumerate(x):
            if y == 3 or y == 4:
                main_board[idx_x][idx_y] = 0

    for idx_y, y in enumerate(main_board[column]):
        # places the current shadow
        if y == 0:
            main_board[column][idx_y] = current_player + 2
            return None


# checks to see if either player has won after every move
# Returns True either player has won, else returns False
def check_win(board, player) -> bool:
    # horizontal test
    for x_idx in range(board_width - 3):
        for y_idx in range(board_height):
            if board[x_idx][y_idx] == player and board[x_idx + 1][y_idx] == player and \
                    board[x_idx + 2][y_idx] == player and board[x_idx + 3][y_idx] == player:
                return True

    # vertical test
    for x_idx in range(board_width):
        for y_idx in range(board_height - 3):
            if board[x_idx][y_idx] == player and board[x_idx][y_idx + 1] == player and \
                    board[x_idx][y_idx + 2] == player and board[x_idx][y_idx + 3] == player:
                return True

    # diagonal up to left test
    for x_idx in range(board_width - 3):
        for y_idx in range(3, board_height):
            if board[x_idx][y_idx] == player and board[x_idx + 1][y_idx - 1] == player and \
                    board[x_idx + 2][y_idx - 2] == player and board[x_idx + 3][y_idx - 3] == player:
                return True

    # diagonal down to left test
    for x_idx in range(board_width - 3):
        for y_idx in range(board_height - 3):
            if board[x_idx][y_idx] == player and board[x_idx + 1][y_idx + 1] == player and \
                    board[x_idx + 2][y_idx + 2] == player and board[x_idx + 3][y_idx + 3] == player:
                return True


def end_game(player: int) -> str:
    # Determines which player won
    if player == 1:
        return 'Red'
    else:
        return 'Yellow'


# starts the game. Does not end until the window is closed
def start_game():
    draw_board(screen, main_board, winner='')

    current_player = 1

    running = True
    winner = ''
    game_over = False
    while running:
        for event in pygame.event.get():

            # stops code if the window is closed
            if event.type == pygame.QUIT:
                running = False

            # handles the player moves
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                column = (pos[0] - 10) // cell_size

                if column in [0, 1, 2, 3, 4, 5, 6]:  # checks to make sure the board was clicked and not the side
                    if place_piece(main_board, column, current_player):
                        if check_win(main_board, current_player):  # checks to see if the player has won
                            print(f'{current_player} has won')
                            winner = end_game(current_player)
                            game_over = True
                            draw_board(screen, main_board, winner)

                        current_player = 3 - current_player  # changes current turn of players
                        place_shadow(column, current_player)  # makes shadow seamless

            # detects mouse movement to draw the shadow
            elif event.type == pygame.MOUSEMOTION and not game_over:
                pos = pygame.mouse.get_pos()
                column = (pos[0] - 10) // cell_size
                if column in [0, 1, 2, 3, 4, 5, 6]:
                    place_shadow(column, current_player)

            # draws board after each turn
            draw_board(screen, main_board, winner)

    # ensures that pygame ends when the window is closed
    pygame.quit()


# starts the game
if __name__ == '__main__':
    pygame.init()
    start_game()
