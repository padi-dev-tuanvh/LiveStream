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

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def output():
    while True:
        threadNo = recvall(ClientSocket, 16).decode("utf-8")
        length = recvall(ClientSocket, 16).decode("utf-8")
        stringData = recvall(ClientSocket, int(length))
        data = np.frombuffer(stringData, dtype="uint8")
        imgdec = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("Client " + threadNo, imgdec)
        q = cv2.waitKey(1)
        if q == ord("q"):
            break
    ClientSocket.close()

Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))

out = threading.Thread(target = output)
out.start()