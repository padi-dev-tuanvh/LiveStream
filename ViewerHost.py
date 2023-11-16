import socket
import threading
import cv2
import numpy as np

class ViewerHost:
    def __init__(self) -> None:
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

    def recvall(self, count):
        buf = b''
        while count:
            newbuf = self.ClientSocket.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def output(self):
        while True:
            threadNo = self.recvall( 16).decode("utf-8")
            length = self.recvall( 16).decode("utf-8")
            stringData = self.recvall( int(length))
            data = np.frombuffer(stringData, dtype="uint8")
            imgdec = cv2.imdecode(data, cv2.IMREAD_COLOR)
            cv2.imshow("Viewer " + threadNo, imgdec)
            q = cv2.waitKey(1)
            if q == ord("q"):
                cv2.destroyAllWindows()
                break
        self.ClientSocket.close()
        cv2.destroyAllWindows()