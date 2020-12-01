import socket
import thread
import sys

server = "192.168.1.230"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server started")

pos = [(0, 0), (100, 100)]


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: {}".format(data))
                print("Sending: {}".format(reply))

            conn.sendall(str.encode(make_pos(reply)))
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
