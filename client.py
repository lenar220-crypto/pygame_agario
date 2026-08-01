import socket
import time
import pygame

width = 800
height = 600

fps = 30
screen_center = (width//2, height//2)

mouse = pygame.mouse

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
con.connect(("localhost", 10000))

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("bugteries")

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if mouse.get_focused():
        pos = mouse.get_pos()
        print(pos)

        vector = (pos[0]-screen_center[0], pos[1]-screen_center[1])
        print(vector)


    con.send("online in python 😱".encode())

    a = con.recv(1024).decode()
    print("сообщение от сервера:", a)

pygame.quit()
