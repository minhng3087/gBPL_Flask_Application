import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    username = os.environ.get("DATABASE_USERNAME")
    password = os.environ.get("DATABASE_PASSWORD")
    port = os.environ.get("DATABASE_PORT")
    dbname = os.environ.get("DATABASE_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@localhost:{port}/{dbname}"
    # 'postgresql://postgres:17071608@localhost:5432/FlaskApp'

    SQLALCHEMY_TRACK_MODIFICATIONS = False