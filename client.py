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

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("bugteries")

screen.fill((150, 150, 150))
pygame.draw.circle(screen, color, screen_center, ball_raduis)

run = True
while run:
    clock.tick(fps)
    pygame.display.flip()

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

    a = con.recv(2048).decode()
    print("сообщение от сервера:", a)

pygame.quit()
