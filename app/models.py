import datetime
from hashlib import md5
import bcrypt
from app import login
from app import db
from flask_login import UserMixin

class Review(db.Model):
    __tablename__ = 'reviews'
    fk_user_from = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fk_user_to = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    content = db.Column(db.String(256))
    score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

class User(UserMixin, db.Model):
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

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))