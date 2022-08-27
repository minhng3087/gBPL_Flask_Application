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
    return {200: "OK"}

@app.route('/home')
def home():
    if current_user.is_authenticated:
        users = User.query.filter(User.id != current_user.id).all()
        return render_template('home.html', title='Home', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not bcrypt.checkpw(form.password.data.encode('utf8'), user.password.encode('utf8')):
            flash("Email/Password is invalid.", 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
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
            flash("The email is existed. Please use another email.", 'danger')
            return redirect(url_for('signup'))

        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)

 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    user = current_user
    
    return render_template("profile.html", title="Profile", user=user)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    pass

@app.route('/search/users', methods=["GET", "POST"])
def search_users():
    if request.method == 'POST':
        search_word = request.form['query']
        search = "%{}%".format(search_word)
        print(search)
        users = User.query.filter(User.name.like(search)).filter(User.id != current_user.id).all()
        # print(users)
    # return jsonify([user.selialize() for user in users])
    return render_template('components/user-home.html', users=[user.selialize() for user in users])

from app.seeds import create_data
@app.route("/seed")
def seed_data():
    create_data()
    return redirect('/')


@app.route("/susume/users", methods=["GET", "POST"])
def susume_users():

    user = the_most_setsuzoku_user(3)
    return {200: "1"}
