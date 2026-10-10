from tkinter import ttk, messagebox
import tkinter as tk

import socket
import pygame
import math

colors = [
    'Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
    'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
    'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
    'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue',
    'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue'
]

width = 800
height = 600

ball_raduis = 50
#ball_speed

name = ""
color = ""

root = tk.Tk()
root.title = "menu"
root.geometry("400x300")

style = ttk.Style()
style.theme_use("clam")

name_label = tk.Label(root, text="введи ник")
name_label.pack()

entry = tk.Entry(root, width=40, justify="center")
entry.pack()

color_label = tk.Label(root, text="\nвыбери цвет")
color_label.pack()


def select(event):
    global color
    color = combo.get()

    style.configure("TCombobox", fieldbackground=color, background="white")

combo = ttk.Combobox(root, values=colors, textvariable=color)
combo.pack()

root.bind("<<ComboboxSelected>>", select)


def play():
    global name

    name = entry.get()

    if name == "" or color == "":
        tk.messagebox.showerror("ошибка", message="не написал имя или цвет")
        return

    root.destroy()
    root.quit()

play_button = tk.Button(root, text="играть", command=play)
play_button.pack(pady=10)



root.mainloop()

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
font = pygame.font.SysFont("arial", 10)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("bugteries")

def find_plrs(vector:str):
    if msg[0:13] == "visible_plrs<":
        start_index = 13

        for index, char in enumerate(msg[13:]):
            if char == ">":
                total = msg[start_index:index]
                return total

def draw_plrs(total:str):
    dict = total.split(" ")
    print("d:",dict)

    setted = []

    for index in dict:
        part = index.split(",")
        print("p:",part)

        x = int(part[0])+screen_center[0]
        y = int(part[1])+screen_center[1]

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
        text_surface = font.render(name, True, (255, 255, 255))

        part_size = size // 2
        screen.blit(text_surface, (x + part_size, y + part_size))

run = True
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

        if vector_len <= ball_raduis:
            pos = (0, 0)

        if old_pos != pos:
            con.send(f"<{pos[0]},{pos[1]}>".encode())
            old_pos = pos

    msg = con.recv(2048).decode()
    #print("сообщение от сервера:", msg)

    total = find_plrs(msg)
    if total:
        draw_plrs(total)

    '''
    if msg[0:14] == "visible_plrs<":
        start_index = 14
        end_index = None

        total = None

        for index, char in enumerate(msg):
            if char == "]" and not end_index:
                end_index = index
                into_info = msg[start_index:end_index]

                a = into_info.split(", ")
                total = list(a)

                break

        setted = []

        for part in total:
            batch = part.split(",")
            print(batch)

            name = batch[2]
            if name in setted:
                print("уже есть")
                continue
            else:
                setted.append(name)

            color = batch[3]

            x = batch[0]

            if x[0] == "'":
                print("неверное число")
                continue
            else:
                x = int(float(x))

            y = int(float(batch[1]))

            size = batch[4]
            size = int(size[0:len(size)-1])

            pygame.draw.circle(screen, color, (x, y), size)
            text_surface = font.render(name, True, (255, 255, 255))

            part_size = size//2
            screen.blit(text_surface, (x+part_size, y+part_size))
    '''

pygame.quit()