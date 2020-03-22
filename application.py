import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# db = SQLAlchemy(app)

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

# class Users(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False)
#     password = db.Column(db.String, nullable=False)

class Users(object):
    query = db.query_property()

@app.route("/")
def index():
    return "Project 1: TODO"

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
        return render_template("error.html", message="Password doesn't match")
    user = db.execute("SELECT * FROM users WHERE username = :username",
                      {"username": username}).first()

    if user:
        return render_template("error.html", message="User already exist")

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


