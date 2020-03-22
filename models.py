from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


# class Passenger(db.Model):
#     __tablename__ = "passengers"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
