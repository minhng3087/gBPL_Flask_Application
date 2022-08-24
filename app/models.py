import datetime
import os
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from app import db

# restaurant_dish = db.Table('reviews',
#     db.Column('reviewer_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('reviewed_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('content',db.String(256)),
#     db.Column('score',db.Integer),
#     db.Column('created_at', db.DateTime),
#     db.Column('modified_at', db.DateTime),
#  )

class Review(db.Model):
    __tablename__ = 'reviews'
    fk_user_from = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fk_user_to = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    content = db.Column(db.String(256))
    score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user_to = db.relationship('Review',backref='to', primaryjoin=id==Review.fk_user_to)
    user_from = db.relationship('Review',backref='from', primaryjoin=id==Review.fk_user_from)
    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__set_password(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def __set_password(self, password):
        pwhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return pwhash.decode('utf8')        

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

