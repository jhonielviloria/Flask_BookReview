import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

LOGGED_IN = False

class Users(object):
    query = db.query_property()


def get_user(username):
    return db.execute("SELECT * FROM users WHERE username = :username",
               {"username": username}).first()


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
        pw = db.execute("select crypt(:login_pass, :user_pass)",
                   {"login_pass": password, "user_pass": user.password}).first()
        if pw[0] != user.password:
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

    # Add passenger.
    db.execute("INSERT INTO users (username, password) VALUES (:username, crypt(:password, gen_salt('bf', 8)))",
               {"username": username, "password": password2,})
    db.commit()
    # user = Users(username=username,
    #              password=password2)
    # db.session.add(user)
    # db.session.commit()
    # flight.add_passenger(name)
    return render_template("registered.html")


