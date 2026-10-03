import psycopg2
from psycopg2.extras import DictCursor

conect = psycopg2.connect("postgresql://postgres:123@localhost:5433/game")

def create_table():
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('''create table if not exists gamers (
                           id serial primary key not null,
                           name varchar(250) not null,
                           color varchar(50) not null,
                           
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
        self.x += self.speed_x
        self.y += self.speed_y

        update_db_pos(self.id, self.x, self.y)

    def change_speed(self, vector):
        info = find(vector)
        #print(info)

        if info == "":
            return

        if info[0] == 0 and info[1] == 0:
            self.speed_x = 0
            self.speed_y = 0

        else:
            self.speed_x = info[0]*self.absolute_speed
            self.speed_y = info[1] * self.absolute_speed


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
            total = list(map(float, a)) # при float оно ломается


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