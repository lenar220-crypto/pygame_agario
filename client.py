import registation

import playsound3
import threading

import socket
import pygame

import math
import json
import time

import os

width = 800
height = 600

ball_raduis = 50
life_time = 0

color = ""
name = ""

registation.gui()

with open("info.json", "r", encoding="utf-8") as file:
    data = json.load(file)

color = data.get("color", color)
name = data.get("name", name)

os.remove("info.json")
playsound3.playsound("sounds/start.mp3")

fps = 30
screen_center = (width//2, height//2)

mouse = pygame.mouse
old_pos = None

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
con.connect(("localhost", 10000))

con.send(f"nac:<{name},{color}>".encode())

pygame.init()
clock = pygame.time.Clock()

fonts = [
    pygame.font.SysFont("arial", 10),
    pygame.font.SysFont("arial", 25)
]

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("bugteries")

run = True
def lifetime_timer():
    global life_time

    while run:
        life_time += 1
        time.sleep(1)

def walk_sound():
    playsound3.playsound("sounds/walk.wav")

def find_plrs():
    if msg[0:13] == "visible_plrs<":
        start_index = 13

        for index, char in enumerate(msg):
            if char == ">":
                total = msg[start_index:index]
                return total

def draw_plrs(total:str):
    dict = total.split(" ")
    setted = []

    for index in dict:
        part = index.split(",")

        x = int(float(part[0]))+screen_center[0]
        y = int(float(part[1]))+screen_center[1]

        try:
            size = int(part[4])
        except:
            continue

        name = part[2]
        if name in setted:
            continue
        else:
            setted.append(name)

        pygame.draw.circle(screen, part[3], (x, y), size)
        text_surface = fonts[0].render(name, True, (255, 255, 255))

        part_size = size // 2
        screen.blit(text_surface, (x + part_size, y + part_size))

threading.Thread(target=lifetime_timer, daemon=True).start()

while run:
    clock.tick(fps)
    pygame.display.flip()

    screen.fill((150, 150, 150))
    pygame.draw.circle(screen, color, screen_center, ball_raduis)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if mouse.get_focused():
        pos = mouse.get_pos()
        pos = (pos[0]-screen_center[0], pos[1]-screen_center[1])

        x_in = pos[0] * pos[0]
        y_in = pos[1] * pos[1]

        vector_len = math.sqrt(x_in + y_in)

        pos = (pos[0]/vector_len, pos[1]/vector_len)

        if vector_len <= ball_raduis: pos = (0, 0)

        if old_pos != pos:
            con.send(f"<{pos[0]},{pos[1]}>".encode())
            old_pos = pos

            threading.Thread(target=walk_sound, daemon=True).start()

    msg = con.recv(2048).decode()
    #print("сообщение от сервера:", msg)

    total = find_plrs()
    if total: draw_plrs(total)

    text_surface = fonts[1].render(f"life time: {life_time}", True, (255, 255, 255))
    screen.blit(text_surface, (0, 0))

    pygame.draw.circle(screen, (0, 0, 0), mouse.get_pos(), 10)

pygame.quit()