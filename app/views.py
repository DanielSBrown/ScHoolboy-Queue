"""
The general views for the music queue and webapp
"""
import random
import string
from flask import jsonify, redirect, request, render_template, make_response
from app import app
from .database import connect_to_db, create_new_room, disconnect_db
from .database import get_all_songs, check_table_exists, fetch_current_songs
from .database import add_new_song, delete_table, get_next_song


@app.route('/health/')
def healthcheck():
    """ Endpoint to make sure the webapp is healthy """
    return 'Healthy\n', 200

@app.route('/room/new/', methods=['POST'])
def new_room():
    """
    Generates a new random room id and creates the table in the database
    """
    room_id = ''.join(random.SystemRandom().choice(
        string.ascii_uppercase))
    room_id += ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(5))
    conn = connect_to_db()
    create_new_room(conn, room_id)
    disconnect_db(conn)

    return jsonify(room=room_id)


@app.route('/room/add/', methods=['POST'])
def queue_song():
    """
    Add a song to the queue
    """

    room = request.values['room']
    song = 'youtube.com/watch?v='
    song += request.values['song_url']
    conn = connect_to_db()
    add_new_song(conn, room, song)
    disconnect_db(conn)
    return redirect('/group/?groupcode={}'.format(room))


@app.route('/room/delete/', methods=['POST'])
def delete_room():
    '''
    Delete a room from the db
    '''
    room = request.values['room']
    conn = connect_to_db()
    delete_table(conn, room)
    disconnect_db(conn)
    return jsonify(status=200)


@app.route('/queued/', methods=['GET'])
def queued():
    """
    Fetches the two next songs queued for a room
    """
    room_id = request.values['room']
    conn = connect_to_db()
    queue = fetch_current_songs(conn, room_id)
    disconnect_db(conn)
    if not queue:
        resp = {'room': room_id, 'current': False, 'next': False}
    elif len(queue) == 1:
        resp = {'room': room_id, 'current': queue[0], 'next': False}
    else:
        resp = {'room': room_id, 'current': queue[0], 'next': queue[1]}
    return jsonify(**resp)


@app.route('/room/pop/', methods=['POST'])
def pop_song():
    room_id = request.values['room']
    conn = connect_to_db()
    get_next_song(conn, room_id)
    disconnect_db(conn)
    return 200



# home page
# group code inputted here
@app.route('/')
def landing():
    """ landing page """
    return render_template('landing.html')

@app.route('/query/')
def query():
    """query page"""
    return render_template('query.html')

# login page
# needs to verify user and password validity
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """ Login Page """
    return redirect('/')

# page when group code entered
# needs to verify groupcode
# should display group name, queue, group members
@app.route('/group/', methods=['GET', 'POST'])
def group():
    """ The main page of the app where each individual queue will be managed """
    groupcode = request.values['groupcode']
    conn = connect_to_db()
    if not check_table_exists(conn, groupcode):
        return redirect('/')
    queue = get_all_songs(conn, groupcode)
    disconnect_db(conn)
    return render_template('group.html', **{'groupcode': groupcode,
                                            'queue': queue})

# page for user profile
# should display user's groups
@app.route('/profile/', methods=['GET', 'POST'])
def user_profile():
    """ Do we need this? I don't know how persistent groups will be """
    name = request.cookies.get('name')
    # password = request.cookies.get('password')
    return render_template('profile.html', name=name)

# cookie is set after sign up or log in
@app.route('/setcookie/', methods=['POST', 'GET'])
def setcookie():
    """ Set the login cookie """
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        resp = make_response(render_template('profile.html'))
        resp.set_cookie('name', name)
        resp.set_cookie('password', password)
        return redirect('/profile/')


# signup page
# needs to verify if user already exists
@app.route('/signup/')
def signup():
    """ The landing page for users to sign up """
    return redirect('/')
