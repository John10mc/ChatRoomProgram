import sys
import socket
import threading
import json
from tkinter import *
import time

class Client():

    def __init__(self, name, ip_address, port, chatroom):
        self.name = name
        self.host_ip = ip_address
        self.host_port = port
        self.chatroom = chatroom
        # create a socket object
        self.my_socket = socket.socket()
        # using the socket object connect to the server given the ip address and port
        self.my_socket.connect((ip_address, port))
        # create a dictionary with config data along with a message saying the username has joing the chatroom
        data = {"name": self.name,
                "chatroom": self.chatroom,
                "message": name + " has joined the chatroom " + chatroom}
        # parse the above dictionary to a JSON string and send it to the server
        self.my_socket.send(json.dumps(data).encode())
        
class Gui():

    def __init__(self):
        # create a window for the user to input data to connect to a server
        self.connect_window = Tk()
        # set the title of the window
        self.connect_window.title("Connect")
        # set the size of the window
        self.connect_window.geometry("400x300")
        # place holders for input for the connect_window window
        self.name = None
        self.address = None
        self.port = None
        self.chatroom = None

        # place holder for a Client Object
        self.client = None
        # flag used to indicate that a thread has to exit
        self.kill = False

        # place holder for the chat window opened after that connect_window
        self.chat_window = None
        # placeholder for the Text box on the chat_window
        self.output = None
        # placeholder for the Entry box on the chat_window
        self.message_box = None

        # call the display_connect() method to display the connect_window to the user
        self.display_connect()

    # method to create a Client object based on what the user has input into the connect_window
    def connect(self):
        # get the text from the text fields on the connect_window
        name_text = self.name.get()
        address_text = self.address.get()
        port_text = self.port.get()
        chatroom_text = self.chatroom.get()
        # create a Client object based on the information the user entered into the connect_window
        self.client = Client(name_text, address_text, int(port_text), chatroom_text)
        # create a thread to continualloy look from messages from the server
        t1 = threading.Thread(target=self.awaitMessage).start()
        # close the connect_window
        self.connect_window.destroy()
        # call the display_chat() method to display the chat_window to the user
        self.display_chat()

    # a protocol is set up to handle the user closing the window and calls on_closing to handle the event
    def on_closing(self):
        # send a dictionary parsed to JSON to the server with the key "kill" to indicate to the server that this connection is closing 
        data = {"kill": True}
        self.client.my_socket.send(json.dumps(data).encode())
        # set the flag kill to true to indicate to a running thread to stop
        self.kill = True
        # close the chat_window
        self.chat_window.destroy()
        exit()

    # method to handle the client sending a message to the server and is called when the Send button is pushed
    def send_message(self):
        # get the text from the output Entry box
        message = self.message_box.get()
        # dont allow th user to send empty strings
        if message != "":
            # send a dictionary parsed to JSON to the server with the message in it
            data = {"message": message}
            self.client.my_socket.send(json.dumps(data).encode())
            # clear the input message box
            self.message_box.delete(0, "end")
            # enable the output box so that data can be entered into it
            self.output.configure(state="normal")
            # add the data to the output box
            self.output.insert(END, "Me: " + message + "\n")
            # disable the output box so that the user cant type text into it
            self.output.configure(state="disabled")

    # method is its own thread to wait for incoming messages
    def awaitMessage(self):
        # allow the GUI to be displayed
        time.sleep(1)
        # add a message to the output box indicating what chat room they are in
        self.client.host_ip, self.client.chatroom
        self.output.insert(END, "Connected to " + self.client.host_ip + ":" + str(self.client.host_port) + " in chatroom " + self.client.chatroom + "\n")
        # disable the output box so that the user cant type text into it
        self.output.configure(state="disabled")
        # continually accept incoming messages
        while True:
            #read the data sent by the server. Will be a json string so parse it to a dictionary
            data = json.loads(self.client.my_socket.recv(1024).decode())
            # if the kill flag is true then break out ofthe loop and exit the thread
            if self.kill:
                break
            # enable the output box so that data can be entered into it
            self.output.configure(state="normal")
            # add the message from the server to the output box
            self.output.insert(END, data["message"] + "\n")
            # disable the output box so that the user cant type text into it
            self.output.configure(state="disabled")

    # method to set up the connect_window
    def display_connect(self):
        # add a label to connect_window followed by a Entry box expecting the clients username
        Label(self.connect_window, text="Please enter your name", fg="black", font="none 12 bold").grid(row=0, column=0, padx=10, sticky=W)
        self.name = Entry(self.connect_window, width=20, bg="white")
        # set the position of the Entry box
        self.name.grid(row=1, column=0, padx=10, sticky=W)
        # set the focus to this Entry box so that user doesnt have to click it
        self.name.focus_set()

        # add a label to connect_window followed by a Entry box expecting the servers address
        Label(self.connect_window, text="Please enter the sever address", fg="black", font="none 12 bold").grid(row=2, column=0, padx=10, sticky=W)
        self.address = Entry(self.connect_window, width=20, bg="white")
        # set the position of the Entry box
        self.address.grid(row=3, column=0, padx=10, sticky=W)

        # add a label to connect_window followed by a Entry box expecting the servers port number
        Label(self.connect_window, text="Please enter the port", fg="black", font="none 12 bold").grid(row=4, column=0, padx=10, sticky=W)
        self.port = Entry(self.connect_window, width=20, bg="white")
        # set the position of the Entry box
        self.port.grid(row=5, column=0, padx=10, sticky=W)

        # add a label to connect_window followed by a Entry box expecting the chatroom they wish to chat in
        Label(self.connect_window, text="Please enter the chatroom", fg="black", font="none 12 bold").grid(row=6, column=0, padx=10, sticky=W)
        self.chatroom = Entry(self.connect_window, width=20, bg="white")
        # set the position of the Entry box
        self.chatroom.grid(row=7, column=0, padx=10, sticky=W)

        # button to accept the above data and call the connect() method when clicked
        Button(self.connect_window, text="Submit", width=0, command=self.connect).grid(row=8, column=0, padx=10, sticky=W)

        # display the window and continue to do untill submit button is clicked or the window is closed
        self.connect_window.mainloop()

    def display_chat(self):
        # create a window for the user to send messages and view recieved messages
        self.chat_window = Tk()
        # set the title of the window to the ip address of the server and the chatroom the are chatting in
        self.chat_window.title("Server: {}/{}".format(self.client.host_ip, self.client.chatroom))

        # add a label to chat_window followed by a Text box Where the recieved and sent messages are displayed
        Label(self.chat_window, text="Messages", fg="black", font="none 12 bold").grid(row=0, column=2, padx=10, sticky=W)
        # set the state to disabled so that the user cant type in it
        self.output = Text(self.chat_window, width=78, height=10, wrap=WORD, background="white")
        # set the position of the Entry box
        self.output.grid(row=1, column=2, padx=10, sticky=W)

        # add a label to chat_window followed by a Text box where a user can type messages to send
        Label(self.chat_window, text="Type your message below", fg="black", font="none 12 bold").grid(row=2, column=2, padx=10, sticky=W)
        self.message_box = Entry(self.chat_window, width=71, bg="white")
        # set the position of the Entry box
        self.message_box.grid(row=3, column=2, padx=10, ipady=20, sticky=W)

        # add a button to the chat_window that whwn the user clicks will call the send_message method
        Button(self.chat_window, text="Send", width=0, command=self.send_message).grid(row=4, column=2, padx=10, sticky=W)

        # protocol used to handle the window being closed. Calles the method on_closing()
        self.chat_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # display the window and continue to do until the window is closed
        self.chat_window.mainloop()

def main():
    windows = Gui()

if __name__ == '__main__':
    main()