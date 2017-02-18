"""
The general views for the music queue and webapp
"""
import random
import string
from flask import jsonify
from app import app
from .database import connect_to_db, create_new_room, disconnect_db


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
