import sys
import socket
import threading
import json

class Server():

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = {}
        self.my_socket.bind((ip_address, port))
        self.my_socket.listen()
        print("Server started on {}:{}".format(ip_address, port))

    def awaitConnections(self):
        while True:
            connection, address = self.my_socket.accept()
            data = json.loads(connection.recv(1024).decode())
            self.connections[connection] = {"name": data["name"],
                                            "chatroom": data["chatroom"]}
            self.broadcast(data["message"], connection)
            threading.Thread(target=self.awaitMessage, args=(connection,)).start()

    def broadcast(self, message, client):
        #print("Here")
        for connection in self.connections:
            if connection != client and self.connections[connection]["chatroom"] == self.connections[client]["chatroom"]:
                data = {"message": message}
                connection.send(json.dumps(data).encode())

    def awaitMessage(self, connection):
        while True:
            data = json.loads(connection.recv(1024).decode())
            self.broadcast((self.connections[connection]["name"] +  ": " + data["message"]), connection)
def main():
    if len(sys.argv) == 3:
        ip_address = sys.argv[1]
        port = int(sys.argv[2])
    else:
        ip_address = "0.0.0.0"
        port = 8080

    server = Server(ip_address, port)
    connections = threading.Thread(target=server.awaitConnections).start()



if __name__ == '__main__':
    main()