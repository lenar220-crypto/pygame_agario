import socket
import time
import datetime
import player_module

player_module.create_table()

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
con.bind(("localhost", 10000))
con.setblocking(False)
con.listen(5)

print(f"создался: {datetime.datetime.now().minute}.{datetime.datetime.now().second}.{datetime.datetime.now().microsecond}")

players = {}

while True:
    try:
        new_con, addres = con.accept()
        print("зашёл", addres)

        new_con.setblocking(False)
        player = player_module.create_player("dd", addres)
        l_player = player_module.L_player(player.id, player.name, player.address, new_con)

        players[player.id] = l_player

    except BlockingIOError:
        pass

    for plr_id in list(players.keys()):
        try:
            bytes = players[plr_id].sock.recv(2048).decode()
            print("сообщение:", bytes)

        except:
            #print("не получилось")
            pass

    for plr_id in list(players.keys()):
        try:
            players[plr_id].sock.send("wake up".encode())
            print("отправил сообщение клиенту")

        except:
            players[plr_id].sock.close()
            del players[plr_id]
            player_module.delete_player(plr_id)

            print("вышел")

    time.sleep(1)