import socket
import time

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
con.connect(("localhost", 10000))

while True:
    time.sleep(2)
    con.send("online in python 😱".encode())
