import datetime
from hashlib import md5
import bcrypt
from app import login
from app import db
from flask_login import UserMixin


user_hobby = db.Table('user_hobby',
                    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                    db.Column('hobby_id', db.Integer, db.ForeignKey('hobbies.id'))
                    )
class Review(db.Model):
    __tablename__ = 'reviews'

    fk_user_from = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fk_user_to = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    content = db.Column(db.String(256))
    score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, primary_key=True)

    def __init__(self, data):
        """
        Class constructor
        """
        self.fk_user_from = data.get('fk_user_from')
        self.fk_user_to = data.get('fk_user_to')
        self.content = data.get('content')
        self.score = data.get("score")
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

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
    icon = db.Column(db.Text())
    description = db.Column(db.Text())
    department = db.Column(db.String(128))
    hobbies = db.relationship('Hobby', secondary=user_hobby, backref='users')
    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__set_password(data.get('password'))
        self.icon = data.get('icon')
        self.department = data.get('department')
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


    def selialize(self):
        return {
            'name': self.name,
            'email': self.email,
        }

    @classmethod
    def seed(cls, fake):
        user = User(
            name = fake.name(),
            email = fake.email(),
            password = cls.__set_password(fake.password()),
        )
        user.save()

    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

class Hobby(db.Model): 
    __tablename__ = 'hobbies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

