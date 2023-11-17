# Server code for 2-player game using sockets
import socket # Network interfacing
from _thread import * # Managing multiple clients
import pickle # Serialize objects
from game import Game # Game to play

# SERVER: Manages game state, client connections, and
# updates the game depending on client actions.

# Threads use importance: Allows for multiple clients
# to be handled concurrently. Without threading, the
# clients would have to wait for each other's processes
# to finish which would be too slow and inconvenient.

server = "127.0.0.1"  # or server = "localhost"
port = 5555 # Port for server to connect to

# TCP socket: server and clients communicate over network
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to address and port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Wait for 2 connections
s.listen(2)
print("Waiting for a connection, Server Started")

connected = set() # Connected clients
games = {} # Game instances
idCount = 0 # Players connected or disconnected

# Connects clients in separate threads
# Updates game state
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


# Accepts incoming connections
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1 # New player connected
    p = 0
    # Is player 0 or 1?
    gameId = (idCount - 1)//2
    # Player 0: Start new game
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    # Player 1: Game ready, start it
    else:
        games[gameId].ready = True
        p = 1

    # Thread creation to handle each client
    start_new_thread(threaded_client, (conn, p, gameId))