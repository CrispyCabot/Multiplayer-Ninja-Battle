#ip 10.93.35.120
import socket
from _thread import *
import sys
import time
import pickle
from player import Player
from config import SCREEN_HEIGHT, SCREEN_WIDTH

server = "10.93.35.120"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

global players
players = [Player(0), Player(1)]

currentPlayer = 0

def threaded_client(conn, player):
    global players, currentPlayer
    conn.send(pickle.dumps(players[player]))
    reply = ""
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
            
                print(player, "Received: ", data)
                print(player, "Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    currentPlayer -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1