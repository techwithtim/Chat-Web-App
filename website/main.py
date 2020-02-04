from flask import Flask, session
from flask_socketio import SocketIO
import time
from flask_sqlalchemy import SQLAlchemy
from website import db, create_app
from models import Message

# setup flask application
app = create_app()
socketio = SocketIO(app)  # used for user communication


# COMMUNICATION FUNCTIONS

@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    keys = dict(json)
    print(keys)
    #save_message(dict(json).message)
    socketio.emit('message response', json)


# DATABASE FUNCTIONS

def save_message(msg):
    if "name" not in session:
        return
    name = session["name"]
    message = Message(name=name, content=msg,time=time.time())
    db.session.add(message)
    db.session.commit()

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