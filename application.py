import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import db, User, Book

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

LOGGED_IN = False


def get_user(username):
    return User.query.filter_by(username=username).first()


@app.route("/")
def index():
    global LOGGED_IN
    if LOGGED_IN:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))


@app.route("/home", methods=["POST", "GET"])
def home():
    global LOGGED_IN
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = get_user(username)
        if not user:
            home_url = "not-registered"
            return render_template("login.html", error_message="Username does not exist!")

        pw_matched = User.query.\
            filter_by(username=username).\
            filter_by(password=func.crypt(password, user.password)).\
            count()
        if not pw_matched:
            return render_template("login.html", error_message="Wrong password")

        LOGGED_IN = True
        return render_template("home.html")
    else:
        if LOGGED_IN:
            return render_template("home.html")
        else:
            return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    global LOGGED_IN
    LOGGED_IN = False
    return redirect(url_for("login"))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/registered", methods=["POST"])
def registered():
    # Get form information.
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("password2")

    if password != password2:
        return render_template("register.html", error_message="Password doesn't match")
    user = get_user(username)

    if user:
        return render_template("register.html", error_message="User already exist")

    new_user = User(username=username,
                    password=func.crypt(password2, func.gen_salt('bf', 8)))
    db.session.add(new_user)
    db.session.commit()

    return render_template("registered.html")


@app.route("/results", methods=["POST"])
def results():
    # Get form information.
    title = request.form.get("title")
    author = request.form.get("author")
    isbn = request.form.get("isbn")
    # titles = db.execute("\\dt")
    # if title:
    #     titles = db.execute("SELECT * FROM Books WHERE title = :title",
    #                                {"title": title}).fetchall()
    # if author:
    #     authors = db.execute("SELECT * FROM Books WHERE author = :author",
    #                                {"author": author}).fetchall()
    # if isbn:
    #     isbns = db.execute("SELECT * FROM Books WHERE title = :isbn",
    #                        {"isbn": isbn}).fetchall()
    # return render_template("results.html", titles=titles)
    return render_template("results.html")