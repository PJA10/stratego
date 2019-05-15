from GameObj import *
from Globals import *
import pygame
import sys



class Spy(GameObj):
    rank = SPY

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


class Scout(GameObj):
    rank = SCOUT

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)

    def get_possible_move_locs(self, board):
        possible_move_locs = []
        row, col = self.row, self.col

        while 0 <= row+1 < board_rows and 0 <= col < board_cols:
            row += 1
            target = board[row][col]
            if not target or (target != 'Lake' and target.owner.id != self.owner.id):
                possible_move_locs.append((row, col))
            if target:
                break

        row, col = self.row, self.col

        while 0 <= row-1 < board_rows and 0 <= col < board_cols:
            row -= 1
            target = board[row][col]
            if not target or (target != 'Lake' and target.owner.id != self.owner.id):
                possible_move_locs.append((row, col))
            if target:
                break

        row, col = self.row, self.col

        while 0 <= row + 1 < board_rows and 0 <= col + 1 < board_cols:
            col += 1
            target = board[row][col]
            if not target or (target != 'Lake' and target.owner.id != self.owner.id):
                possible_move_locs.append((row, col))
            if target:
                break

        row, col = self.row, self.col

        while 0 <= row < board_rows and 0 <= col - 1 < board_cols:
            col -= 1
            target = board[row][col]
            if not target or (target != 'Lake' and target.owner.id != self.owner.id):
                possible_move_locs.append((row, col))
            if target:
                break

        return possible_move_locs


class Miner(GameObj):
    rank = MINER

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


class Sergeant(GameObj):
    rank = SERGEANT

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


class Lieutenant(GameObj):
    rank = LIEUTENANT

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


class Captain(GameObj):
    rank = CAPTAIN

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


class Major(GameObj):
    rank = MAJOR

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


class Colonel(GameObj):
    rank = COLONEL

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


class General(GameObj):
    rank = GENERAL

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


class Marshal(GameObj):
    rank = MARSHAL

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)

class Bomb(GameObj):
    rank = 0

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)


    def get_possible_move_locs(self, board, steps=0):
        return []



class Flag(GameObj):
    rank = "F"

    def __init__(self, board, row, col, owner):
        super().__init__(board, row, col, owner)

    def dead(self, board):
        super().dead(board)
        print("Player", 1-self.owner.id, "won")

    def get_possible_move_locs(self, board, steps=0):
        return []
