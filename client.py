import socket
import time
import pygame
import math

width = 800
height = 600

ball_raduis = 50
#ball_speed

fps = 30
screen_center = (width//2, height//2)

mouse = pygame.mouse
old_pos = None

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
con.connect(("localhost", 10000))

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("bugteries")

screen.fill((150, 150, 150))
pygame.draw.circle(screen, (255, 0, 0), screen_center, ball_raduis)
pygame.display.flip()

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if mouse.get_focused():
        pos = mouse.get_pos()
        print(pos)

        pos = (pos[0]-screen_center[0], pos[1]-screen_center[1])

        x_in = pos[0] * pos[0]
        y_in = pos[1] * pos[1]

        vector_len = math.sqrt(x_in + y_in)

        pos = (pos[0]/vector_len, pos[1]/vector_len)

        if vector_len <= ball_raduis:
            pos = (0, 0)

        if old_pos != pos:
            con.send(f"<{pos[0]},{pos[1]}>".encode())
            old_pos = pos

    a = con.recv(2048).decode()
    print("сообщение от сервера:", a)

pygame.quit()
