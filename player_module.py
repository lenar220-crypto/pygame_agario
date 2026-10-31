from datetime import time

import psycopg2
from psycopg2.extras import DictCursor

import time
import random
import threading

import registation

colors = registation.colors
bot_count = 30

conect = psycopg2.connect("postgresql://postgres:123@localhost:5433/game")

def create_table():
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('''create table if not exists gamers (
                           id serial primary key not null,
                           name varchar(250) not null,
                           color varchar(50) not null default 'red',
                           
                           w_vis integer default 800,
                           h_vis integer default 600,
                           
                           address varchar not null,
                           
                           x integer default 500,
                           y integer default 500,
                           
                           size integer default 50,
                           errors integer default 0,
                           
                           absolute_speed integer default 1,
                           speed_x integer default 0,
                           speed_y integer default 0
                       );
        ''')

    conect.commit()

class Player:
    def __init__(self, id, address, name="?", color="Red", w_vis=800, h_vis=600, x=500, y=500, size=50, errors=0, absolute_speed=1, speed_x=0, speed_y=0):
        self.id = id
        self.name = name
        self.color = color

        self.w_vis = w_vis
        self.h_vis = h_vis

        self.address = address

        self.x = x
        self.y = y

        self.size = size
        self.errors = errors

        self.absolute_speed = absolute_speed
        self.speed_x = speed_x
        self.speed_y = speed_y

class L_player:
    def __init__(self, id, name, address, sock, color="Red", w_vis=800, h_vis=600, x=500, y=500, size=50, errors=0, absolute_speed=2, speed_x=2, speed_y=2):
        self.id = id
        self.name = name
        self.color = color

        self.w_vis = w_vis
        self.h_vis = h_vis

        self.address = address
        self.sock = sock
        self.x = x
        self.y = y
        self.size = size
        self.errors = errors
        self.absolute_speed = absolute_speed
        self.speed_x = speed_x
        self.speed_y = speed_y

        self.db:Player = get_player(id)

    def update(self):
        try:
            zero = 0+self.size
            other = 4000-self.size

            if self.x <= zero:
                if self.speed_x >= 0:
                    self.x += self.speed_x
                    update_db_pos(self.id, self.x, self.y)

            elif self.x >= other:
                if self.speed_x <= 0:
                    self.x += self.speed_x
                    update_db_pos(self.id, self.x, self.y)

            else:
                self.x += self.speed_x
                update_db_pos(self.id, self.x, self.y)

            if self.y <= zero:
                if self.speed_y >= 0:
                    self.y += self.speed_y
                    update_db_pos(self.id, self.x, self.y)

            elif self.y >= other:
                if self.speed_y <= 0:
                    self.y += self.speed_y
                    update_db_pos(self.id, self.x, self.y)

            else:
                self.y += self.speed_y
                update_db_pos(self.id, self.x, self.y)
        except:
            pass

    def change_speed(self, vector):
        info = find(vector)

        if info == "":
            return

        if info[0] == 0 and info[1] == 0:
            self.speed_x = 0
            self.speed_y = 0

        else:
            self.speed_x = info[0]*self.absolute_speed
            self.speed_y = info[1] * self.absolute_speed

    def update_all(self):
        print("upd")

        '''
        with conect.cursor(cursor_factory=DictCursor) as cursor:
            text = "update gamers set x = %s, y = %s, name = %s, color = %s, absolute_speed = %s, speed_x = %s, speed_y = %s, w_hiv = %s, h_vis = %s where id = %s;"
            cursor.execute(text, (self.x, self.y, self.name, self.color, self.absolute_speed, self.speed_x, self.speed_y, self.w_vis, self.h_vis, self.id))
        '''

        with conect.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(f"update gamers set x = {self.x}, y = {self.y}, name = {self.name}, color = {self.color}, absolute_speed = {self.absolute_speed}, speed_x = {self.speed_x}, speed_y = {self.speed_y}, w_hiv = {self.w_vis}, h_vis = {self.h_vis} where id = {self.id};")

        conect.commit()

def join_find(info):
    start_index = None
    end_index = None

    for index, char in enumerate(info):
        if char == "<":
            start_index = index

        elif char == ">" and start_index is not None:
            end_index = index
            into_info = info[start_index + 1:end_index]

            total = into_info.split(",")

            return total[0], total[1]

    return ""

def find(vector:str):
    start_index = None
    end_index = None

    for index, char in enumerate(vector):
        if char == "<":
            start_index = index

        elif char == ">" and start_index is not None:
            end_index = index
            into_info = vector[start_index+1:end_index]

            a = into_info.split(",")
            total = list(map(float, a))


            return total

    return ""

def create_player(name, address):
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        text = "insert into gamers (name, address) values (%s, %s) returning *"
        cursor.execute(text, (name, address))

        to_return = cursor.fetchone()

    conect.commit()

    return Player(*to_return)

def get_player(plr_id):
    with conect.cursor() as cursor:
        text = "select * from gamers where id = %s"
        cursor.execute(text, (plr_id,))

        return Player(*cursor.fetchone())

def delete_player(plr_id):
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        text = "delete from gamers where id = %s"
        cursor.execute(text, (plr_id,))

    conect.commit()
    print(plr_id)

def delete_all():
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("truncate table gamers")

    conect.commit()

def update_db_pos(plr_id, new_x, new_y):
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        text = "update gamers set x = %s, y = %s where id = %s;"
        cursor.execute(text, (new_x, new_y, plr_id))

    conect.commit()

def update_db_name_and_color(plr_id, new_name, new_color):
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        text = "update gamers set name = %s, color = %s where id = %s;"
        cursor.execute(text, (new_name, new_color, plr_id))

    conect.commit()

def bot_move(bot):
    while bot:
        speed = random.randint(-bot.absolute_speed, bot.absolute_speed)
        speed2 = random.randint(-bot.absolute_speed, bot.absolute_speed)

        bot.speed_x = speed
        bot.speed_y = speed2

        time.sleep(random.randint(1, 5))

def create_bot(name, size):
    bot = create_player(name, "")

    bot.name = name
    bot.color = random.choice(colors)

    bot.x = random.randint(100, size)
    bot.y = random.randint(100, size)

    bot.size = random.randint(25, 75)

    speed = random.randint(1, 3)
    bot.absolute_speed = speed

    l_bot = L_player(id=bot.id, address="", sock="", name=bot.name, color=bot.color, x=bot.x, y=bot.y, size=bot.size)
    threading.Thread(target=lambda: bot_move(l_bot), daemon=True).start()

    return l_bot