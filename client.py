import sys
import socket
import threading
import json

class Client():

    def __init__(self, name, ip_address, port, chatroom):
        self.name = name
        self.host_ip = ip_address
        self.host_port = port
        self.chatroom = chatroom
        self.my_socket = socket.socket()
        self.my_socket.connect((ip_address, port))
        data = {"name": self.name,
                "chatroom": self.chatroom,
                "message": name + " has joined the chatroom " + chatroom}
        self.my_socket.send(json.dumps(data).encode())
        print("Connected to {}:{}".format(ip_address, port))
        t1 = threading.Thread(target=self.awaitMessage).start()
        t2 = threading.Thread(target=self.sendMessages).start()

    def awaitMessage(self):
        while True:
            data = json.loads(self.my_socket.recv(1024).decode())
            print(data["message"])

    def sendMessages(self):
        while True:
            message = input()
            data = {"message": message}
            self.my_socket.send(json.dumps(data).encode())

def main():

    if len(sys.argv) == 5:
        client = Client(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        "Please enter the correct arguements in the form <name> <ip Address> <port number>"

    #client.my_socket.close()


if __name__ == '__main__':
    main()