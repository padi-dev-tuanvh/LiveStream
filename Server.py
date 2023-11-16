import socket
from _thread import *

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host = host_ip
port = 1234
socket_address = (host, port)
ThreadCount = 0
threads = []

try:
    ServerSocket.bind(socket_address)
except socket.error as e:
    print(str(e))
print('Waiting for a Connection..')
ServerSocket.listen(5)
print("Listening at:",socket_address)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def threaded_client(connection, addr):
    connection.sendall(str.encode('\n\nWelcome to the Server\n\n'))
    while True:
        if connection:
            length = recvall(connection, 16)
            stringData = recvall(connection, int(length))        
        for i in range(ThreadCount):
            (client, address) = threads[i]
            if addr != address:
                if client:
                    thread = addr
                    client.sendall(str.encode(str(ThreadCount).ljust(16))) # New
                    client.sendall(length)
                    client.sendall(stringData)  
            else:
                if client:
                    client.sendall(str.encode(str(ThreadCount).ljust(16)))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print("Client:\n", Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    threads.append((Client, ThreadCount))
    start_new_thread(threaded_client, (Client, ThreadCount))
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()