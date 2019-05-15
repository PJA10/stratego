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
            g = self.client.recv(32768*4)
            #print(g)
            #print(pickle.loads(g))
            self.client.send(b'1')
            b = self.client.recv(32768*8)
            #print(b)
            #print(pickle.loads(b))
            return pickle.loads(g), pickle.loads(b)
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            msg = pickle.dumps(data)
            #print(msg)
            #print(pickle.loads(msg))
            self.client.send(pickle.dumps(data))
            got = self.client.recv(32768*16)
            #print('got:', got)
            #print(pickle.loads(got))
            ret = pickle.loads(got)
            return ret
        except socket.error as e:
            print(e)

    def close(self):
        self.client.close()