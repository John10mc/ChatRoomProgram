import sys
import socket
import threading
import json

class Server():

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        # create a socket object that uses IPv4 addresses and expects data through TCP
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # dictionary that contains data on the active connections
        self.connections = {}
        # bind the passed ip address and port to the socket
        self.my_socket.bind((ip_address, port))
        # allow the socket to listen for incoming connections
        self.my_socket.listen()
        print("Server started on {}:{}".format(ip_address, port))
        #create a thread to actively look for incoming connections
        threading.Thread(target=self.awaitConnections).start()

    def awaitConnections(self):
        # continually accept incoming connections
        while True:
            # accept a connection and save its data
            connection, address = self.my_socket.accept()
            # first message recieved will be congif data about the connection such as username and chatroom
            data = json.loads(connection.recv(1024).decode())
            # store the config data about the connection
            self.connections[connection] = {"name": data["name"],
                                            "chatroom": data["chatroom"]}
            # broadcast that a new user has joined the chatroom to all other users in that chatroom
            self.broadcast(data["message"], connection)
            # spawn a thread that will continually look for messages from the new clients. Each client will have its own thread for this
            t = threading.Thread(target=self.awaitMessage, args=(connection,)).start()

    def broadcast(self, message, client):
        # loop through all the active connections
        for connection in self.connections:
            # if the connection is not itself and its the right chatroom then send the message to that connection
            if connection != client and self.connections[connection]["chatroom"] == self.connections[client]["chatroom"]:
                # create a dictionary to store the data to be sent
                data = {"message": message}
                # convert the dictionary to a JSON string and send it to the connection
                connection.send(json.dumps(data).encode())

    # method is its own thread for each incoming connection
    def awaitMessage(self, connection):
        # continually accept incoming messages
        while True:
            #read the data sent by the client. Will be a json string so parse it to a dictionary
            data = json.loads(connection.recv(1024).decode())
            # if the dictionary contains a key "kill" them the connection is no longer active
            if "kill" in data:
                # broadcast to all the other clients in the same chatroom that this client has left the chatroom
                self.broadcast(self.connections[connection]["name"] +  " has left the chatroom", connection)
                # send an empty string so that the client can exit its awaitMessage method in client.py
                connection.send(json.dumps("").encode())
                # remove this connection from the active connections
                del self.connections[connection]
                break
            else:
                # broadcast to all the other clients in the same chatroom the recieved message
                self.broadcast((self.connections[connection]["name"] +  ": " + data["message"]), connection)

def main():
    # if the correct number of arguements are not passed then go to the default
    if len(sys.argv) == 3:
        ip_address = sys.argv[1]
        port = int(sys.argv[2])
    else:
        ip_address = "0.0.0.0"
        port = 8080

    # create a Server object to start the server
    server = Server(ip_address, port)
    # close the socket and free the port for other porcesses
    #server.my_socket.close()

if __name__ == '__main__':
    main()