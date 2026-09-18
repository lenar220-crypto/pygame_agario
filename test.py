'''

















































'''

import tkinter as tk
from playsound3 import playsound
import threading
import time
import pyautogui

root = tk.Tk()
root.attributes('-fullscreen', True)


frames = [
    "materials/frame1.png",
    "materials/frame2.png",
    "materials/frame3.png"
]

def sound():
    playsound('materials/Unknown_artist_-_KOROCHE_CHITY_-_BAN_OSKORBLENIE_-_BAN_(SkySound7.com).mp3')

label = tk.Label(root)
label.pack()

def animation_thread():
    for x in range(14):
        for frame_path in frames:
            photo = tk.PhotoImage(file=frame_path)

            label.config(image=photo)
            label.image = photo

            time.sleep(0.2)

    pyautogui.press("escape")

def close_escape(event):
    label.config(image="")
    root.destroy()

root.bind("<Escape>", close_escape)

threading.Thread(target=sound, daemon=True).start()
threading.Thread(target=animation_thread, daemon=True).start()

root.mainloop()