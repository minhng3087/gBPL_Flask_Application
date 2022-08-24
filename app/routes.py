from flask import jsonify
from flask import request
from flask import render_template
from flask import redirect
from flask import flash
from flask import url_for
from flask_login import current_user, login_user, logout_user

from app.forms import SignupForm
from app.forms import LoginForm
from app import app
from app.models import *
from app.helpers import *

@app.route('/')
def index():
    return {200:"OK"}

@app.route('/index')
def home():
    return render_template('home.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not bcrypt.checkpw(form.password.data.encode('utf8'), user.password.encode('utf8')):
            flash("Email/Password is invalid.")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')
    return render_template('login.html', title='Log In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate():
        data = {
            "name": form.username.data,
            "email": form.email.data,
            "password": form.password.data,
        }
        user = User(data)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("The email is existed. Please use another email.")
            return redirect(url_for('signup'))

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Add new user', form=form)

 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))