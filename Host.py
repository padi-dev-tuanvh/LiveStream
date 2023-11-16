import socket
import threading
import cv2
import numpy as np

ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host = host_ip
port = 1234

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def inputs():
    while True:
        vid = cv2.VideoCapture(0) # change to 0 if access camera
        while vid.isOpened():
            ret, img = vid.read()
            res, imgenc = cv2.imencode(".jpg", img, encode_params)
            data = np.array(imgenc)
            stringData = data.tobytes()
            cv2.imshow("Host",img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if ClientSocket:
                ClientSocket.sendall(str.encode(str(len(stringData)).ljust(16)))
                ClientSocket.sendall(stringData)
        vid.release()
        cv2.destroyAllWindows()
    

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))

inp = threading.Thread(target = inputs)
inp.start()