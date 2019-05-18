from Player import *


class Game:

    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.revealed_pieces = []
        self.turn = 0
        self.animation = None
        self.winner = None

        self.board = []
        for row_num in range(board_rows):
            row = []
            for col_num in range(board_cols):
                if 4 <= row_num <= 5 and (2 <= col_num <= 3 or 6 <= col_num <= 7):
                    row.append("Lake")
                else:
                    row.append(None)

            self.board.append(row)


    def play(self, data):
        loc = (int(data[1][0]),int(data[1][1]))
        result = data[0].move(self.board, loc)
        if isinstance(result, tuple) and result[0] == "win":
            self.winner = data[0].owner.id
            self.revealed_pieces.append(loc)
            self.revealed_pieces.append((data[0].row, data[0].col))
        elif isinstance(result, Animation):
            self.revealed_pieces.append(loc)
            self.revealed_pieces.append((data[0].row,data[0].col))
            self.animation = result
        else:
            self.revealed_pieces = []
        self.turn = 1- self.turn



class Animation:

    def __init__(self, end, just_died, winner):
        self.end = end
        self.just_died = just_died
        self.winner = winner
        self.start = 1
        if winner:
            self.direction =  (end[0] - winner.row, end[1] - winner.col)
        else:
            self.direction = (end[0] - just_died[0].row, end[1] - just_died[0].col) if (end[0] - just_died[0].row, end[1] - just_died[0].col) != (0,0) else (end[0] - just_died[1].row, end[1] - just_died[1].col)
        self.direction = (self.direction[0]//max(1,abs(self.direction[0])), self.direction[1]//max(1, abs(self.direction[1])))

        self.id =self.just_died[0].owner.id
        if self.winner:
            self.id = self.winner.owner.id
        else:
            for dead in just_died:
                if dead.row != self.end[0] or dead.col != self.end[1]:
                    self.id = dead.owner.id
        self.id = 1 -self.id

