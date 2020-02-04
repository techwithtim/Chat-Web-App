from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from flask_socketio import SocketIO, join_room, leave_room, send
from jinja2 import  Undefined

# GLOBAL CONSTANTS
NAME_KEY = 'name'

# GLOBAL VARS
client = None
messages = []

# setup flask application
app = Flask(__name__)
app.secret_key = "hellomynamestimandyouwontguessthis"
socketio = SocketIO(app)  # used for user communication

# APP ROUTES

@app.route("/login", methods=["POST","GET"])
def login():
    """
    displays main login page and handles saving name in session
    :exception POST
    :return: None
    """
    if request.method == "POST":  # if user input a name
        name = request.form["inputName"]
        if len(name) >= 2:
            session[NAME_KEY] = name
            flash(f'You were successfully logged in as {name}.')
            return redirect(url_for("home"))
        else:
            flash("1Name must be longer than 1 character.")

    return render_template("login.html", **{"session":"session"})


@app.route("/logout")
def logout():
    """
    logs the user out by popping name from session
    :return: None
    """
    session.pop(NAME_KEY, None)
    flash("You were logged out.")
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    """
    displays home page if logged in
    :return: None
    """
    global client

    if NAME_KEY not in session:
        return redirect(url_for("login"))

    return render_template("index.html", **{"session": session})


@app.route("/get_name")
def get_name():
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


# COMMUNICATION FUNCTIONS

@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('message response', json, callback=message_received)


def message_received(methods=['GET', 'POST']):
    print('message was received!!!')


# Handle Rooms

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


# JINJA TEMPLATE FILTERS
@app.context_processor
def slice():
    def _slice(iterable, pattern):
        if iterable is None or isinstance(iterable, Undefined):
            return iterable

        # convert to list so we can slice
        items = str(iterable)

        start = None
        end = None
        stride = None

        # split pattern into slice components
        if pattern:
            tokens = pattern.split(':')
            print(tokens)
            if len(tokens) > 1:
                start = int(tokens[0])
            if len(tokens) > 2:
                end = int(tokens[1])
            if len(tokens) > 3:
                stride = int(tokens[2])

        return items[start:end:stride]
    return dict(slice=_slice)


# MAINLINE

if __name__ == "__main__":
    socketio.run(app, debug=True, host="192.168.0.21")