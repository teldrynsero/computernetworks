import socket
import pickle

# NETWORK: Manages client-side network
# communication with the server. With this class,
# clients can connect to server, send data, and
# receive responses. 

class Network:
    def __init__(self):
        # Client-side connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Server IP address
        self.server = "127.0.0.1"
        # Port server is listening
        self.port = 5555
        # Server's address and port
        self.addr = (self.server, self.port)
        # Player ID obtained from server
        self.p = self.connect()

    # Get player ID
    def getP(self):
        return self.p

    # Connect to server using provided address
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    # Send data to server
    def send(self, data):
        try: # Encode data then send to server
            self.client.send(str.encode(data))
            # Receives server response, deserializes received data
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

