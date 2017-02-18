from sqlite3 import connect


def connect_to_db():
    conn = connect('ScHoolboy_Queue.sqlite')
    return conn


def disconnect_db(conn):
    conn.close()
    return


def create_new_room(conn, room_name):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS {}'.format(room_name))
    cursor.execute('CREATE TABLE {} (song TEXT, pos INTEGER)'.format(room_name))
    conn.commit()


def add_new_song(conn, room_name, song):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM {}'.format(room_name))
    count = cursor.fetchone()[0]
    insert = 'INSERT INTO {} VALUES (?, ?)'.format(room_name)
    cursor.execute(insert, (song, count))
    conn.commit()


def delete_table(conn, room_name):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS {}'.format(room_name))
    conn.commit()

def get_next_song(conn, room_name):
    cursor = conn.cursor()
    cursor.execute('SELECT * from {} where pos=0'.format(room_name))
    song = cursor.fetchone()[0]
    cursor.execute('DELETE FROM {} WHERE pos=0'.format(room_name))
    cursor.execute('UPDATE {} SET pos = pos - 1'.format(room_name))
    return song
