import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "46.117.245.207"
        self.port = 1234
        self.addr = (self.server, self.port)
        self.player, self.game= self.connect()

    def get_player(self):
        return self.player

    def get_game(self):
        return self.game

    def connect(self):
        try:
            self.client.connect(self.addr)
            g = recv(self.client)
            #print(g)
            #print(pickle.loads(g))
            self.client.send(b'1')
            b = recv(self.client)
            #print(b)
            #print(pickle.loads(b))
            return g, b
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            #print(msg)
            #print(pickle.loads(msg))
            send_msg(self.client, data)
            got = recv(self.client)
            #print('got:', got)
            #print(pickle.loads(got))
            return got
        except socket.error as e:
            print(e)

    def close(self):
        self.client.close()


def get_len(msg):
    return str(len(msg)).ljust(20)

def send_msg(conn , msg):
    msg_b = pickle.dumps(msg)
    len_msg = get_len(msg_b).encode('utf-8')
    conn.sendall(len_msg + msg_b)

def recv(conn):
    msg_len = int(conn.recv(20))
    recved = b""
    while len(recved) < msg_len:
        recved = recved + conn.recv(msg_len-len(recved))
    ret = pickle.loads(recved)
    return ret