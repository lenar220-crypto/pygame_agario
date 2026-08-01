import socket
import time

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
con.bind(("localhost", 10000))
con.setblocking(False)
con.listen(5)

print("создался")

players = []

while True:
    try:
        new_con, addres = con.accept()
        print("зашёл", addres)

        new_con.setblocking(False)
        players.append(new_con)

    except BlockingIOError:
        pass

    for player in players:
        try:
            bytes = player.recv(1024).decode()
            print("сообщение:", bytes)

        except:
            #print("не получилось")
            pass

    for player in players:
        try:
            player.send("wake up".encode())
            print("отправил сообщение клиенту")

        except:
            players.remove(player)
            player.close()

            print("вышел")

    time.sleep(1)