import socket
import pygame

import player_module
import russian_names

player_module.create_table()

bot_count = player_module.bot_count
names = russian_names.RussianNames(count=bot_count*2, patronymic=False, surname=False, rare=True)
names = set(names)
names = list(names)

game_width = 4000
game_height = 4000

screen_width = 600
screen_height = 600

fps = 100

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 10)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("admin panel")

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
con.bind(("localhost", 10000))
con.setblocking(False)
con.listen(5)

players = {}

for num in range(bot_count):
    bot = player_module.create_bot(names[num], game_width)

    players[bot.id] = bot

run = True
while run:
    clock.tick(fps)

    try:
        new_con, addres = con.accept()
        print("зашёл", addres)

        join_info = new_con.recv(2048).decode()

        new_con.setblocking(False)
        player = player_module.create_player("dd", addres)

        if join_info[0:3] == "nac":
            name, color = player_module.join_find(join_info)

            player.name = name
            player.color = color

        l_player = player_module.L_player(player.id, player.name, player.address, new_con, player.color)
        player_module.update_db_name_and_color(l_player.id, l_player.name, l_player.color)
        players[player.id] = l_player

    except BlockingIOError:
        pass

    for plr_id in list(players.keys()):
        try:
            bytes = players[plr_id].sock.recv(2048).decode()
            #print("сообщение:", bytes)
            #print("байты:", bytes)

            players[plr_id].change_speed(bytes)

        except:
            pass

    visible_plrs = {}
    for plr_id in list(players.keys()):
        visible_plrs[plr_id] = []

    players_list = list(players.items())

    for x in range(0, len(players_list)):
        for y in range(x+1, len(players_list)):

            try:
                player1:player_module.L_player = players_list[x][1]
                player2:player_module.L_player = players_list[y][1]

                dist_x = player2.x-player1.x
                dist_y = player2.y-player1.y

                dist_x2 = abs(dist_x)
                dist_y2 = abs(dist_y)

                if player1.h_vis//2+player2.size >= dist_y2 and player1.w_vis+player2.size >= dist_x2:
                    visible_plrs[player1.id].append(f"{dist_x},{dist_y},{player2.name},{player2.color},{player2.size}")

                if player2.h_vis//2+player1.size//2 >= dist_y2 and player2.w_vis+player1.size >= dist_x2:
                    visible_plrs[player2.id].append(f"{-dist_x},{-dist_y},{player1.name},{player1.color},{player1.size}")
            except:
                pass

    for plr_id in list(players.keys()):
        info = f"visible_plrs<{" ".join(visible_plrs[plr_id])}>"

        if visible_plrs[plr_id] == []:
            continue

        try:
            players[plr_id].sock.send(info.encode())
        except:
            pass


    for plr_id in list(players.keys()):
        try:
            players[plr_id].sock.send("wake up".encode())
            #print("отправил сообщение клиенту")

        except:
            try:
                players[plr_id].sock.close()
                del players[plr_id]
                player_module.delete_player(plr_id)
            except:
                pass

            print("вышел")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0, 0, 0))

    for plr_id in list(players.keys()):
        plr = players[plr_id]

        players[plr_id].update()

        x = screen_width*plr.x//game_width
        y = screen_height*plr.y//game_width

        size = screen_width*plr.size//game_width
        pygame.draw.circle(screen, plr.color, (x, y), size)

        part_size = size//2
        text_surface = font.render(plr.name, True, (255, 255, 255))
        screen.blit(text_surface, (x+part_size, y+part_size))

    pygame.display.flip()

player_module.delete_all()
con.close()
pygame.quit()