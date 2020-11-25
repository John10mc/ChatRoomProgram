from tkinter import *


def click():
    entered_text = textentry.get()
    output.delete(0.0, END)
    output.insert(END, entered_text)

def close_window():
    window.destroy()
    exit()

window = Tk()
window.title("ChatBox")
Label(window, text="Please enter your name", fg="black", font="none 12 bold").grid(row=0, column=0, sticky=W)
textentry = Entry(window, width=20, bg="white")
textentry.grid(row=1, column=0, sticky=W)

Label(window, text="Please enter the sever address", fg="black", font="none 12 bold").grid(row=2, column=0, sticky=W)
textentry2 = Entry(window, width=20, bg="white")
textentry2.grid(row=3, column=0, sticky=W)

Label(window, text="Please enter the port", fg="black", font="none 12 bold").grid(row=4, column=0, sticky=W)
textentry3 = Entry(window, width=20, bg="white")
textentry3.grid(row=5, column=0, sticky=W)

Button(window, text="Submit", width=0, command=click).grid(row=6, column=0, sticky=W)

output = Text(window, width=75, height=6, wrap=WORD, background="white")
output.grid(row=7, column=0, columnspan=2, sticky=W)

Button(window, text="Exit", width=0, command=close_window).grid(row=8, column=0, sticky=W)



window.mainloop()