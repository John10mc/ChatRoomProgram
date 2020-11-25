import sys
import socket
import threading

class Server():

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.my_socket.bind((ip_address, port))
        self.my_socket.listen()
        print("Server started on {}:{}".format(ip_address, port))

    def awaitConnections(self):
        while True:
            connection, address = self.my_socket.accept()
            name = connection.recv(1024).decode()
            self.connections.append((connection, name))
            threading.Thread(target=self.awaitMessage, args=(connection, name)).start()

    def broadcast(self, message, client, name):
        #print("Here")
        for connection in self.connections:
            if connection[0] != client:
                connection[0].send((name +  ": " + message).encode())

    def awaitMessage(self, connection, name):
        while True:
            message = connection.recv(1024).decode()
            self.broadcast(message, connection, name)
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