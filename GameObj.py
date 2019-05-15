from Player import *
import pygame
from Game import *

class GameObj:
    img = None

    def __init__(self, board, row, col, owner):
        self.row = int(row)
        self.col = int(col)
        self.owner = owner
        if self.owner:
            self.owner.soldiers.append(self)

        if board and not board[self.row][self.col]:
            board[self.row][self.col] = self


    def move_to(self, board, target):
        board[self.row][self.col] = None
        if isinstance(target, GameObj):
            self.row = target.row
            self.col = target.col
        board[self.row][self.col] = self

    def __str__(self):
        return str(self.rank)

    def draw(self, screen, x, y, my_player_id):
        if self.owner.id == my_player_id:
            if self.owner.color == blue:
                img = pygame.image.load("img/blue/blue" + str(self.rank) + ".jpg")
                img = pygame.transform.scale(img, (square_size, square_size))
            else:
                img = pygame.image.load("img/red/red" + str(self.rank) + ".jpg")
                img = pygame.transform.scale(img, (square_size, square_size))

            screen.blit(img, (x,y))
        else:
            if self.owner.color == blue:
                img = pygame.image.load("img/blue/blueDefault.jpg")
                img = pygame.transform.scale(img, (square_size, square_size))
            else:
                img = pygame.image.load("img/red/redDefault.jpg")
                img = pygame.transform.scale(img, (square_size, square_size))
            screen.blit(img, (x,y))

    def dead(self, board):
        #board[self.row][self.col] = None
        self.owner.soldiers.remove(self)

    def move(self, board, loc):
        target = board[loc[0]][loc[1]]
        if not target:
            self.move_to(board, GameObj(None, loc[0], loc[1], None))
            return 'empty', []
        elif target == 'Lake' or target.owner == self.owner:
            return None
        elif target.owner != self.owner:
            return self.fight(board, target)
        else:
            print("error in move")

    def fight(self, board, target):
        dead = []
        winner = None
        if target.rank == BOMB and self.rank != MINER:
            self.dead(board)
            winner = target
            dead.append(self)
        elif target.rank == 'F':
            target.dead(board)
            dead.append(target)
            winner = self
            return 'win', dead
        elif self.rank == SPY and target.rank != BOMB:
            target.dead(board)
            dead.append(target)
            winner = self
        elif target.rank == self.rank:
            target.dead(board)
            self.dead(board)
            dead.append(target)
            dead.append(self)
        elif target.rank > self.rank:
            self.dead(board)
            dead.append(self)
            winner = target
        elif target.rank < self.rank:
            target.dead(board)
            dead.append(target)
            winner = self
        else:
            print('error in fight')
        return Animation((target.row, target.col), dead, winner)


    def get_possible_move_locs(self, board, steps=1):
        possible_move_locs = []
        for step in range(1, 1+steps):
            row, col = self.row + step, self.col
            if 0 <= row < board_rows and 0 <= col < board_cols:
                target = board[row][col]
                if not target or (target != 'Lake' and target.owner.id != self.owner.id):
                    possible_move_locs.append((row, col))

            row, col = self.row, self.col + step
            if 0 <= row < board_rows and 0 <= col < board_cols:
                target = board[row][col]
                if not target or (target != 'Lake' and target.owner.id != self.owner.id):
                    possible_move_locs.append((row, col))

            row, col = self.row - step, self.col
            if 0 <= row < board_rows and 0 <= col < board_cols:
                target = board[row][col]
                if not target or (target != 'Lake' and target.owner.id != self.owner.id):
                    possible_move_locs.append((row, col))

            row, col = self.row, self.col - step
            if 0 <= row < board_rows and 0 <= col < board_cols:
                target = board[row][col]
                if not target or (target != 'Lake' and target.owner.id != self.owner.id):
                    possible_move_locs.append((row, col))

        return possible_move_locs


