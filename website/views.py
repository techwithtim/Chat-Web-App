from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint

view = Blueprint("views", __name__)

# GLOBAL CONSTANTS
NAME_KEY = 'name'

# GLOBAL VARS
client = None
messages = []


@view.route("/login", methods=["POST","GET"])
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


@view.route("/logout")
def logout():
    """
    logs the user out by popping name from session
    :return: None
    """
    session.pop(NAME_KEY, None)
    flash("You were logged out.")
    return redirect(url_for("login"))


@view.route("/")
@view.route("/home")
def home():
    """
    displays home page if logged in
    :return: None
    """
    global client

    if NAME_KEY not in session:
        return redirect(url_for("login"))

    return render_template("index.html", **{"session": session})


@view.route("/get_name")
def get_name():
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)