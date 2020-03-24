from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os, csv



app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db = SQLAlchemy(app)


class Books(db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)


def main():
    db.create_all()
    with open("books.csv") as f:
        next(f)
        reader = csv.reader(f)
        for isbn, title, author, year in reader:
            book = Books(isbn=isbn, title=title, author=author, year=year)
            db.session.add(book)
            print(f"Added {title}.")
    db.session.commit()

if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()