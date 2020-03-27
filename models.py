import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# from sqlalchemy.ext.declarative import declarative_base


db = SQLAlchemy()

# Base = declarative_base()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Book(db.Model):
    __tablename__ = "Books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Book {}>'.format(self.title)


class Review(db.Model):
    __tablename__ = "Reviews"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    book = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Review {}>'.format(self.id)
