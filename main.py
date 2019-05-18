from Globals import *
from Player import *
from Soldiers import *
import pygame
import sys
from network import Network


def print_board(board):
    for row_num in range(board_rows):
        for col_num in range(board_cols):
            if board[row_num][col_num] == 'Lake':
                print(bcolors.WARNING, end= '')
            print(board[row_num][col_num], end=' ')
            print(bcolors.ENDC, end='')
        print('')
    print('')

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
soldiers_list = [[Flag, 1], [Bomb, 6], [Scout, 8], [Miner, 5], [Sergeant, 4], [Lieutenant, 4], [Captain, 4], [Major, 3], [Colonel, 2], [General, 1], [Marshal, 1], [Spy, 1]]

def main():
    clock = pygame.time.Clock()
    n = Network()
    my_player = n.get_player()
    game = n.get_game()
    my_id = my_player.id
    for player in game.players:
        if player.id == my_id:
            my_player = player

    FPS = 60
    screen.fill(green)
    board = game.board
    my_color = "blue" if my_player.color == blue else "red"

    game_states = "starting"
    curr_soldier_class = 0
    if not my_player.finished_setup:
        created_soldiers = []
        while soldiers_list[-1][1] and game_states != "exit":
            clicked_locations = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_states = "exit"

                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = pygame.mouse.get_pos()
                    # switch 0,1 because (x,y) == (col,row)
                    clicked_locations.append((click_pos[1]//square_size, click_pos[0]//square_size))

            if clicked_locations:
                loc = clicked_locations[0]
                if (my_player.id == 1 and loc[0] < 4) or (my_player.id == 0 and loc[0] > 5):

                    for soldier in created_soldiers:
                        if (soldier.row, soldier.col) == loc:
                            break
                    else:
                        new_soldier = soldiers_list[curr_soldier_class][0](board, loc[0], loc[1], my_player)
                        created_soldiers.append(new_soldier)

                        soldiers_list[curr_soldier_class][1] -= 1
                        if not soldiers_list[curr_soldier_class][1]:
                            curr_soldier_class = min(curr_soldier_class + 1, len(soldiers_list) -1)

            draw_screen(screen, game, my_player, cursor=f"img/{my_color}/{my_color}{soldiers_list[curr_soldier_class][0].rank}.jpg")
            pygame.display.flip()
            clock.tick(FPS)
        if game_states != "exit":
            for soldier in created_soldiers:
                n.send((soldier, (soldier.row, soldier.col)))
            my_player.finished_setup = True

    selected_soldier = None
    possible_move_locs = []

    while game_states != "exit":
        clicked_locations = set()
        try:
            game = n.send("get")
            board = game.board
        except Exception as e:
            #game_states = "exit"
            print("Couldn't get game", e)

        for player in game.players:
            if player.id == my_id:
                my_player = player
            else:
                enemy_player = player

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_states = "exit"

            if event.type == pygame.MOUSEBUTTONUP:
                click_pos = pygame.mouse.get_pos()
                # switch 0,1 because (x,y) == (col,row)
                clicked_locations = clicked_locations.union({(click_pos[1]//square_size, click_pos[0]//square_size)})


        if not game.animation:
            # print(selected_soldier, possible_move_locs, clicked_locations)
            for loc in clicked_locations:
                if selected_soldier:
                    if loc not in possible_move_locs:
                        selected_soldier = None
                        possible_move_locs = []
                    else:
                        game = n.send((selected_soldier, loc))
                        board = game.board
                        selected_soldier = None
                        possible_move_locs = []
                else:
                    if board[loc[0]][loc[1]] and board[loc[0]][loc[1]] != 'Lake'and board[loc[0]][loc[1]].owner.id == game.turn and game.turn == my_player.id:
                        possible_move_locs = board[loc[0]][loc[1]].get_possible_move_locs(board)
                        if possible_move_locs:
                            selected_soldier = board[loc[0]][loc[1]]

        draw_screen(screen, game, my_player, possible_move_locs)
        pygame.display.flip()
        clock.tick(FPS)

        if game.animation:
            if my_id == game.animation.id:
                #print('sleep')
                pygame.time.wait(10)
        if game.winner != None:
            winner(screen, game.winner, my_player)
            game_states = "exit"

    n.close()
    pygame.quit()
    sys.exit()

def winner(screen, winner, my_player):
    game_states = "starting"

    while game_states != "exit":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_states = "exit"

        screen.fill(black)
        text = "you lose"
        if winner == my_player.id:
            text = "you win"

        message_display(screen, text)
        pygame.display.flip()


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()

def message_display(screen, text, x=screen_width / 2, y=screen_height / 2, size=100):
    large_text = pygame.font.SysFont('comicsansms', size)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)


def draw_screen(screen, game, my_player, possible_move_locs=[], cursor=""):
    board = game.board
    screen.fill(green)

    for row_num in range(board_rows):
        for col_num in range(board_cols):
            if board[row_num][col_num] == 'Lake':
                pygame.draw.rect(screen, blue,
                                 pygame.Rect(col_num * square_size, row_num * square_size, square_size, square_size))
            elif board[row_num][col_num]:
                if (row_num, col_num) in game.revealed_pieces or (game.animation and (
                        board[row_num][col_num] in game.animation.just_died or board[row_num][
                    col_num] == game.animation.winner)):
                    board[row_num][col_num].draw(screen, col_num * square_size, row_num * square_size,
                                                 board[row_num][col_num].owner.id)
                else:
                    board[row_num][col_num].draw(screen, col_num * square_size, row_num * square_size, my_player.id)

    for possible_move_loc in possible_move_locs:
        pygame.draw.circle(screen, yellow, (
        possible_move_loc[1] * square_size + square_size // 2, possible_move_loc[0] * square_size + square_size // 2),
                           square_size // 4)

    for row_num in range(1, board_rows):
        y = row_num * square_size
        pygame.draw.line(screen, black, (0, y), (screen_width, y))
    for col_num in range(1, board_cols):
        x = col_num * square_size
        pygame.draw.line(screen, black, (x, 0), (x, screen_height))

    if cursor:
        cursor_img = pygame.image.load(cursor).convert_alpha()
        cursor_img = pygame.transform.scale(cursor_img, (square_size//2, square_size//2))
        x,y = pygame.mouse.get_pos()
        x -= cursor_img.get_width()//2
        y -= cursor_img.get_height()//2
        screen.blit(cursor_img, (x,y))


if __name__ == '__main__':
    main()