import socket
from _thread import *
import sys
from Player import *
import pickle
from Game import *

server = "192.168.1.22"
port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

game = Game()


def threaded_client(conn, player):
    global game
    send = pickle.dumps(game.players[player])
    print(send)
    print(pickle.loads(send))
    conn.sendall(send)
    send = pickle.dumps(game)
    print(send)
    print(pickle.loads(send))
    print(conn.recv(1))
    conn.sendall(send)
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(32768*2))

            if not data:
                print("Disconnected")
                break
            else:
                if data != "get" and data != "r":
                    game.play(data)
                elif data == "r":
                    game.game_status = 'r'
                    for dead in game.just_died:
                        game.board[dead.row][dead.col] = None

                reply = game

            if game.animation and player == game.animation.id:
                animation = game.animation

                if animation.start < 30:
                    animation.start += 1
                else:
                    animation.start = 1
                    if animation.winner:
                        game.board[animation.winner.row][animation.winner.col] = None
                        if (animation.winner.row, animation.winner.col) in game.revealed_pieces:
                            index = game.revealed_pieces.index((animation.winner.row, animation.winner.col))
                            game.revealed_pieces[index] = (game.revealed_pieces[index][0] + animation.direction[0], game.revealed_pieces[index][1] + animation.direction[1])
                        animation.winner.row += animation.direction[0]
                        animation.winner.col += animation.direction[1]
                        game.board[animation.winner.row][animation.winner.col] = animation.winner
                        if animation.winner.row == animation.end[0] and animation.winner.col == animation.end[1]:
                            game.board[animation.just_died[0].row][animation.just_died[0].col] = None
                            game.board[animation.end[0]][animation.end[1]] = animation.winner
                            game.animation = None
                            game.revealed_pieces = [(animation.end[0], animation.end[1])]

                    else:
                        for dead in animation.just_died:
                            if dead.row != animation.end[0] or dead.col != animation.end[1]:
                                if (dead.row, dead.col) in game.revealed_pieces:
                                    index = game.revealed_pieces.index((dead.row, dead.col))
                                    game.revealed_pieces[index] = (game.revealed_pieces[index][0] + animation.direction[0], game.revealed_pieces[index][1] + animation.direction[1])
                                game.board[dead.row][dead.col] = None
                                dead.row += animation.direction[0]
                                dead.col += animation.direction[1]
                                game.board[dead.row][dead.col] = dead

                        if animation.just_died[0].row == animation.just_died[1].row and animation.just_died[0].col == animation.just_died[1].col:
                            game.board[animation.just_died[0].row][animation.just_died[0].col] = None
                            game.animation = None


                #print("Received: ", data)
                #print("Sending : ", reply)
            reply = pickle.dumps(reply)
            #print(reply)
            #print(pickle.loads(reply))
            conn.sendall(reply)
        except Exception as e:
            print("e:", e)
            break

    print("Lost connection")
    conn.close()

def main():
    currentPlayer = 0
    addreses_dict = {}
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        if currentPlayer < 2:
            start_new_thread(threaded_client, (conn, currentPlayer))
            addreses_dict[addr[0]] = currentPlayer
            currentPlayer += 1
        elif addr[0] in addreses_dict:
            start_new_thread(threaded_client, (conn, addreses_dict[addr[0]]))





if __name__ == '__main__':
    main()