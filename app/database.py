"""
Basic Database Functionality
TODO:
    Refactor into an object
    Rearrange the queue
"""
from sqlite3 import connect


def connect_to_db():
    """
    Wrapper function for db connection
    """
    conn = connect('ScHoolboy_Queue.sqlite')
    return conn


def disconnect_db(conn):
    """
    Wrapper function to kill the db
    """
    conn.close()
    return


def create_new_room(conn, room_name):
    """
    Wrapper Function for creation of a new room
    """
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS {}'.format(room_name))
    cursor.execute('CREATE TABLE {} (song TEXT, pos INTEGER)'.format(room_name))
    conn.commit()


def add_new_song(conn, room_name, song):
    """
    Wrapper Function for adding songs to existing queue for a room
    """
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM {}'.format(room_name))
    count = cursor.fetchone()[0]
    insert = 'INSERT INTO {} VALUES (?, ?)'.format(room_name)
    cursor.execute(insert, (song, count))
    conn.commit()


def delete_table(conn, room_name):
    """
    Wrapper function to delete table when a room is finished
    """
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS {}'.format(room_name))
    conn.commit()


def fetch_current_songs(conn, room_name):
    """
    App wants to have information on the currently playing and next song queued
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {} ORDER BY pos ASC LIMIT 2'.format(room_name))
    return [row[0] for row in cursor.fetchall()]


def get_all_songs(conn, room_name):
    """ Get an ordered queue of all songs for a room """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {} ORDER BY pos ASC'.format(room_name))
    return [row[0] for row in cursor.fetchall()]


def get_next_song(conn, room_name):
    """
    Delete the currently queued song and move the remaining songs up
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * from {} where pos=0'.format(room_name))
    song = cursor.fetchone()[0]
    cursor.execute('DELETE FROM {} WHERE pos=0'.format(room_name))
    cursor.execute('UPDATE {} SET pos = pos - 1'.format(room_name))
    conn.commit()
    return song

def check_table_exists(conn, room_name):
    """ Returns a boolean if a table with the given name exists """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(
        room_name))
    return bool(cursor.fetchone())

def create_user(conn, user_name):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS {}'.format(user_name))
    cursor.execute('CREATE TABLE {} (user TEXT, pass INTEGER)'.format(user_name))
    conn.commit()
