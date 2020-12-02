import socket
import thread
from player import Player
import pickle

server = "192.168.1.230"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: {}".format(data))
                print("Sending: {}".format(reply))

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print ("Lost connection")
    conn.close()

current_player = 0

while True:
    conn, addr = s.accept()
    print("Connected to: {}".format(addr))
    thread.start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
