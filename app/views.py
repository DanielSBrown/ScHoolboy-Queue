"""
The general views for the music queue and webapp
"""
import random
import string
from flask import jsonify, redirect, request, render_template, make_response
from app import app
from .database import connect_to_db, create_new_room, disconnect_db
from .database import get_all_songs, check_table_exists


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
        string.ascii_uppercase + string.digits) for _ in range(6))
    conn = connect_to_db()
    create_new_room(conn, room_id)
    disconnect_db(conn)
    return jsonify(room=room_id)


# home page
# group code inputted here
@app.route('/')
def landing():
    """ landing page """
    return render_template('landing.html')

# login page
# needs to verify user and password validity
@app.route('/login/', methods=['GET', 'POST'])
def login():
    """ Login Page """
    return render_template('login.html')

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
    return render_template('signup.html')
