import tkinter as tk
from PIL import Image, ImageTk
import pygame

pygame.mixer.init()
hover = pygame.mixer.Sound('other_files/hover.wav')
click = pygame.mixer.Sound('other_files/click.wav')


def camera():
    click.play()
    print("Camera Access")

def screen():
    click.play()
    print("Screen Access")

def microph():
    click.play()
    print("Microphone Access")

def cmd():
    click.play()
    print("Cmd Access")

def accept_req():
    click.play()
    print("Accepting Requests")

def on_enter(event):
    event.widget.config(bg='red', fg='cyan')
    event.widget.config(bg='red', fg='cyan')
    event.widget.config(bg='red', fg='cyan')
    event.widget.config(bg='red', fg='cyan')
    hover.play()
    

def on_leave(event):
    event.widget.config(bg='red', fg='black')
    event.widget.config(bg='red', fg='black')
    event.widget.config(bg='red', fg='black')
    event.widget.config(bg='red', fg='black')


window = tk.Tk()
window.title("Anonymous Trozan")
window.geometry("650x450+500+200")
window.resizable(False, False)

bg_image_pil = Image.open("./other_files/hackerbg.jpg")
bg_image = ImageTk.PhotoImage(bg_image_pil)
bg_label = tk.Label(window, image=bg_image)
bg_label.place(x=-1, y=-10, relwidth=1, relheight=1)


b1_x = 140
b1_y = 160

button1 = tk.Button(window, text="Camera", command=lambda: camera() , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
button1.place(x=b1_x , y=b1_y)
button1.bind("<Enter>", on_enter)
button1.bind("<Leave>", on_leave)

button2 = tk.Button(window, text="Screen", command=lambda: screen() , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
button2.place(x=b1_x,y=b1_y+100)
button2.bind("<Enter>", on_enter)
button2.bind("<Leave>", on_leave)

button3 = tk.Button(window, text="Microphone", command=lambda: microph() , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
button3.place(x=b1_x+250,y=b1_y)
button3.bind("<Enter>", on_enter)
button3.bind("<Leave>", on_leave)

button4 = tk.Button(window, text="Comand Prompt", command=lambda: cmd() , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
button4.place(x=b1_x+250,y=b1_y+100)
button4.bind("<Enter>", on_enter)
button4.bind("<Leave>", on_leave)

button5 = tk.Button(window, text="Accept Requests", command=lambda: accept_req() , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
button5.place(x=b1_x+100,y=b1_y+200)
button5.bind("<Enter>", on_enter)
button5.bind("<Leave>", on_leave)

window.mainloop()
