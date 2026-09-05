import socket
import time
import datetime
import player_module
import pygame

player_module.create_table()

game_width = 4000
game_height = 4000

screen_width = 600
screen_height = 600

fps = 100

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("admin panel")

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
con.bind(("localhost", 10000))
con.setblocking(False)
con.listen(5)

print(f"создался: {datetime.datetime.now().minute}.{datetime.datetime.now().second}.{datetime.datetime.now().microsecond}")

players = {}

run = True
while run:
    clock.tick(fps)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0, 0, 0))

    for id in list(players.keys()):
        plr = players[id]
        x = game_width//screen_width*plr.x
        y = game_height//screen_height*plr.y

        print(x, y)

        size = game_width//screen_width*plr.size
        pygame.draw.circle(screen, (255, 0, 0), (x, y), size)

    pygame.display.flip()

player_module.delete_all()
con.close()
pygame.quit()