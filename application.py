import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, func, and_, text
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
LOGGED_IN = False
user = None


def main():
    db.create_all()


if __name__=="__main__":
    with app.app_context():
        main()


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
    global user
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
    global user
    LOGGED_IN = False
    user = None
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

    if get_user(username):
        return render_template("register.html", error_message="User already exist")

    new_user = User(username=username,
                    password=func.crypt(password2, func.gen_salt('bf', 8)))
    db.session.add(new_user)
    db.session.commit()

    return render_template("registered.html")


def add_percent(string):
    return('%' + str(string) +'%')


# def get_query(string, category):
#     arg = text('Book.' + category)
#     return Book.query.filter(arg==string).all()


# def get_query_like(string, category):
#     arg = text('Book.' + category + '.ilike("' + add_percent(string) + '")')
#     return Book.query.filter(arg).all()
    # book = Book.query.filter(Book.title.ilike(add_percent(title))).all()

@app.route("/results", methods=["POST"])
def results():
    books = []
    # Get form information.
    title = request.form.get("title")
    author = request.form.get("author")
    isbn = request.form.get("isbn")

    # Get exact matches
    # books += get_query(title, 'title')
    # books += get_query(author, 'author')
    # books += get_query(isbn, 'isbn')
    books += Book.query.filter(Book.title==title).all()
    books += Book.query.filter(Book.author==author).all()
    books += Book.query.filter(Book.isbn==isbn).all()
    # Get like matches
    if title:
        books += Book.query.filter(Book.title.ilike(add_percent(title))).all()
    if author:
        books += Book.query.filter(Book.author.like(add_percent(author))).all()
    if isbn:
        books += Book.query.filter(Book.isbn.ilike(add_percent(isbn))).all()

    # book = get_query_like(isbn, 'isbn')
    # books = set(books)

    if not books:
        return render_template("home.html", error_message="No results found!")
    # Remove duplicates
    books = set(books)

    return render_template("results.html", books=books)


@app.route("/<int:book_id>", methods=['POST', 'GET'])
def book(book_id):
    if request.method == 'GET':
        book_detail = Book.query.get(book_id)
        # return render_template("book.html", book=book_detail)
    else:
        global user
        content = request.form.get("content")
        book_detail = Book.query.get(book_id)
        username = user.username
        print(content)
        print(book_detail)
        print(username)
        if content:
            new_review = Review(content=content,
                                user=username,
                                book=book_detail.title)
            print(new_review)
            db.session.add(new_review)
            print('add')
            db.session.commit()
            print('commit')
        # return redirect(url_for("book"))
    return render_template("book.html",
                           book=book_detail,
                           reviews=Review.query.filter(Review.book==book_detail.title).all())


@app.route("/<int:book_id>")
def book_review(book_id):
    global user
    content = request.form.get("content")
    book_detail = Book.query.get(book_id)
    username = user.username
    if content:
        new_review = Review(content=content,
                            user=username,
                            book=book_detail)
        db.session.add(new_review)
        db.session.commit()
    return redirect(url_for("book"))
    # return render_template("book.html",
    #                        book=book_detail,
    #                        reviews=Review.query.filter(Review.book==book_detail))


