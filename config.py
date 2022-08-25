import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'demo.db')
    username = os.environ.get("DATABASE_USERNAME")
    password = os.environ.get("DATABASE_PASSWORD")
    port = os.environ.get("DATABASE_PORT")
    dbname = os.environ.get("DATABASE_NAME")
    print(port)
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@localhost:{port}/{dbname}"
    print(SQLALCHEMY_DATABASE_URI)
    # 'postgresql://postgres:17071608@localhost:5432/FlaskApp'

    SQLALCHEMY_TRACK_MODIFICATIONS = False