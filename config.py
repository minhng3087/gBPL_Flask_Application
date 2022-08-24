import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'demo.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456789@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False