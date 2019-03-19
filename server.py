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
players = [Player(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-100), Player(SCREEN_WIDTH/2+100, SCREEN_HEIGHT-100)]

def threaded_client(conn, player):
    global players
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

                if reply.reset:
                    if player == 1:
                        players[0] = Player(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-100)
                    else:
                        players[1] = Player(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-100)
                    reply = Player(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-100)
            
                print(player, "Received: ", data)
                print(player, "Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1