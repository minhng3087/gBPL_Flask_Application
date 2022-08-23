import datetime
import os
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from app import db


association_table = db.Table('reviews', db.Model.metadata,
    db.Column('review_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('content', db.String(128)),
    db.Column()
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    children = db.relationship("reviews",secondary=association_table)
    # blogposts = db.relationship('BlogpostModel', backref='users', lazy=True)

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

    def check_hash(self, password):
        return bcrypt.checkpw(self.password.encode('utf8'), password.encode('utf8'))
        # return bcrypt.check_password_hash(self.password, password)

class Review(db.Model):
  __tablename__ = 'reviews'

  id = db.Column(db.Integer, primary_key=True)
  reviewer_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
  content = db.Column(db.String(256))
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.name = data.get('name')
    self.content = data.get('content')
  def __repr(self):
    return '<id {}>'.format(self.id)

