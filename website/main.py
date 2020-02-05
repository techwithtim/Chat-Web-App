from flask import session
from flask_socketio import SocketIO
import time
from application import create_app
from application.database import DataBase

# setup flask application
app = create_app()
socketio = SocketIO(app)  # used for user communication

# COMMUNICATION FUNCTIONS


@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    """
    handles saving messages once received from web server
    and sending message to other clients
    :param json: json
    :param methods: POST GET
    :return: None
    """
    data = dict(json)
    if "name" in data:
        db = DataBase()
        db.save_message(data["name"], data["message"])
    socketio.emit('message response', json)


'''
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
'''

# MAINLINE

if __name__ == "__main__":
    socketio.run(app, debug=True, host="192.168.0.21")