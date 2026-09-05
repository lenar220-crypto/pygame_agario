import psycopg2
from psycopg2.extras import DictCursor

conect = psycopg2.connect("postgresql://postgres:123@localhost:5433/game")

def create_table():
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('''create table if not exists gamers (
                           id serial primary key not null,
                           name varchar(250) not null,
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
    def __init__(self, id, name, address, x=500, y=500, size=50, errors=0, absolute_speed=1, speed_x=0, speed_y=0):
        self.id = id
        self.name = name
        self.address = address
        self.x = x
        self.y = y
        self.size = size
        self.errors = errors
        self.absolute_speed = absolute_speed
        self.speed_x = speed_x
        self.speed_y = speed_y

class L_player:
    def __init__(self, id, name, address, sock, x=500, y=500, size=50, errors=0, absolute_speed=1, speed_x=0, speed_y=0):
        self.id = id
        self.name = name
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

def create_player(name, address):
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        #cursor.execute(f"insert into gamers (name, address) values ('{name}', '{address}') returning *")
        text = "insert into gamers (name, address) values (%s, %s) returning *"
        cursor.execute(text, (name, address))

        to_return = cursor.fetchone()

    conect.commit()

    return Player(*to_return)

def get_player(plr_id):
    with conect.cursor() as cursor:
        text = "select * from gamers where id, = %s"
        cursor.execute(text, (plr_id,))

        return Player(*cursor.fetchone())

def delete_player(plr_id):
    with conect.cursor(cursor_factory=DictCursor) as cursor:
        text = "delete from gamers where id = %s"
        cursor.execute(text, (plr_id,))

    conect.commit()