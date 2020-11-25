import sys
import socket
import threading


class Client():

    def __init__(self, name, ip_address, port):
        self.name = name
        self.host_ip = ip_address
        self.host_port = port
        self.my_socket = socket.socket()
        self.my_socket.connect((ip_address, port))
        self.my_socket.send((name).encode())
        print("Connected to {}:{}".format(ip_address, port))
        t1 = threading.Thread(target=self.awaitMessage).start()
        t2 = threading.Thread(target=self.sendMessages).start()

    def awaitMessage(self):
        while True:
            message = self.my_socket.recv(1024)
            print(message.decode())

    def sendMessages(self):
        while True:
            message = input()
            self.my_socket.send(message.encode())

def main():

    if len(sys.argv) == 4:
        client = Client(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    else:
        "Please enter the correct arguements in the form <name> <ip Address> <port number>"

    #client.my_socket.close()


if __name__ == '__main__':
    main()