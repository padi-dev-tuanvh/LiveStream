import socket
import threading
import cv2
import numpy as np
class HostModel:

    def __init__(self):
        self.ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.host = self.host_ip
        self.port = 1234
        self.encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def connectServer(self):
        print('Waiting for connection')
        try:
            self.ClientSocket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e))

        Response = self.ClientSocket.recv(1024)
        print(Response.decode('utf-8'))


    def recvall(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def inputs(self):
        while True:
            vid = cv2.VideoCapture(0) # change to 0 if access camera
            while vid.isOpened():
                ret, img = vid.read()
                res, imgenc = cv2.imencode(".jpg", img, self.encode_params)
                data = np.array(imgenc)
                stringData = data.tobytes()
                cv2.imshow("Host",img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if self.ClientSocket:
                    self.ClientSocket.sendall(str.encode(str(len(stringData)).ljust(16)))
                    self.ClientSocket.sendall(stringData)
            vid.release()
            cv2.destroyAllWindows()
