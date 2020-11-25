import sys
import socket
import threading
import json
from tkinter import *

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
        

class Gui():

    def __init__(self):
        self.connect_window = Tk()
        self.connect_window.title("Connect")
        self.connect_window.geometry("400x300")
        self.name = None
        self.address = None
        self.port = None
        self.chatroom = None

        self.client = None

        self.chat_window = None
        self.output = None
        self.message_box = None

        self.display_connect()

    def connect(self):
        name_text = self.name.get()
        address_text = self.address.get()
        port_text = self.port.get()
        chatroom_text = self.chatroom.get()
        self.client = Client(name_text, address_text, int(port_text), chatroom_text)
        t1 = threading.Thread(target=self.awaitMessage).start()
        self.connect_window.destroy()
        self.display_chat()

    def send_message(self):
        message = self.message_box.get()
        data = {"message": message}
        self.client.my_socket.send(json.dumps(data).encode())
        self.message_box.delete(0, "end")
        self.output.insert(END, "Me: " + message + "\n")

    def awaitMessage(self):
        while True:
            data = json.loads(self.client.my_socket.recv(1024).decode())
            self.output.insert(END, data["message"] + "\n")

    def display_connect(self):

        Label(self.connect_window, text="Please enter your name", fg="black", font="none 12 bold").grid(row=0, column=0, padx=10, sticky=W)
        self.name = Entry(self.connect_window, width=20, bg="white")
        self.name.grid(row=1, column=0, padx=10, sticky=W)
        self.name.focus_set()

        Label(self.connect_window, text="Please enter the sever address", fg="black", font="none 12 bold").grid(row=2, column=0, padx=10, sticky=W)
        self.address = Entry(self.connect_window, width=20, bg="white")
        self.address.grid(row=3, column=0, padx=10, sticky=W)

        Label(self.connect_window, text="Please enter the port", fg="black", font="none 12 bold").grid(row=4, column=0, padx=10, sticky=W)
        self.port = Entry(self.connect_window, width=20, bg="white")
        self.port.grid(row=5, column=0, padx=10, sticky=W)

        Label(self.connect_window, text="Please enter the chatroom", fg="black", font="none 12 bold").grid(row=6, column=0, padx=10, sticky=W)
        self.chatroom = Entry(self.connect_window, width=20, bg="white")
        self.chatroom.grid(row=7, column=0, padx=10, sticky=W)

        Button(self.connect_window, text="Submit", width=0, command=self.connect).grid(row=8, column=0, padx=10, sticky=W)

        self.connect_window.mainloop()

    def display_chat(self):
        self.chat_window = Tk()
        self.chat_window.title("Server: {}/{}".format(self.client.host_ip, self.client.chatroom))

        Label(self.chat_window, text="Messages", fg="black", font="none 12 bold").grid(row=0, column=2, padx=10, sticky=W)
        self.output = Text(self.chat_window, width=78, height=10, wrap=WORD, background="white")
        self.output.grid(row=1, column=2, padx=10, sticky=W)

        Label(self.chat_window, text="Type your message below", fg="black", font="none 12 bold").grid(row=2, column=2, padx=10, sticky=W)
        self.message_box = Entry(self.chat_window, width=71, bg="white")
        self.message_box.grid(row=3, column=2, padx=10, ipady=20, sticky=W)

        Button(self.chat_window, text="Send", width=0, command=self.send_message).grid(row=4, column=2, padx=10, sticky=W)

        self.chat_window.mainloop()
        self.output.insert("Connected to {}:{} in chatroom {}".format(self.address.get(), self.port.get(), self.chatroom.get()))

    # output.delete(0.0, END)
    # output.insert(END, entered_text)

    # def close_window():
    #     window.destroy()
    #     exit()

def main():

    windows = Gui()

    #output = Text(window, width=75, height=6, wrap=WORD, background="white")
    #output.grid(row=7, column=0, columnspan=2, sticky=W)

    #Button(window, text="Exit", width=0, command=close_window).grid(row=8, column=0, sticky=W)



    

    #client.my_socket.close()


if __name__ == '__main__':
    main()