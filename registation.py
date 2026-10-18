from tkinter import ttk, messagebox
import tkinter as tk

import json

colors = [
    'Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
    'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
    'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
    'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue',
    'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue'
]

color = ""
name = ""
def gui():
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

        info = {
            "color": color,
            "name": name
        }

        with open("info.json", "w", encoding="utf-8") as file:
            json.dump(info, file, indent=4, ensure_ascii=False)

    play_button = tk.Button(root, text="играть", command=play)
    play_button.pack(pady=10)

    root.mainloop()