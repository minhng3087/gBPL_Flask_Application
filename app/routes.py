from app.seeds import create_data
from flask import request
from flask import render_template
from flask import redirect
from flask import flash
from flask import url_for
from flask import session
from flask_login import current_user, login_user, logout_user
from flask_socketio import join_room, leave_room, emit
from app.forms import *
from app import app, socket_app
from app.models import *
from app.helpers import *
from sqlalchemy.sql import func

from app.chat_helpers import *

online_users = [User.query.filter(User.email=="mail0@gmail.com").first()]
online_users_sid = []

@app.route('/')
def index():
    return redirect (url_for("login"))
    return {200: "OK"}
@app.route('/home')
def home():
    print("Online user: ",online_users)
    if current_user.is_authenticated:
        users = User.query.filter(User.id != current_user.id).order_by(User.id).all()
        users_most_connect = the_most_setsuzoku_user(current_user.id)
        users_last_connect = last_setsuzoku_user(current_user.id)
        notices = Notice.query.filter(Notice.to_id == current_user.id).order_by(Notice.id.desc()).limit(3).all()
        print(notices)
        return render_template('home.html', title='Home', 
                                current_user=current_user, users=users, 
                                users_most_connect=users_most_connect, 
                                users_last_connect=users_last_connect,
                                online_users=online_users, 
                                notices=notices
        )
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

        global online_users 
        online_users.append(user)
        print(online_users)
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
            db.sessocket_appn.add(user)
            db.sessocket_appn.commit()
        except Exception:
            db.sessocket_appn.rollback()
            flash("The email is existed. Please use another email.", 'danger')
            return redirect(url_for('signup'))

        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)


@app.route('/logout')
def logout():
    global online_users 
    print(online_users)
    online_users = [u for u in online_users if u.id != current_user.id]
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    user = current_user

    average = Review.query.with_entities(func.avg(Review.score).label('score')).filter(Review.fk_user_to == current_user.id).scalar()

    if average != None:
        average = round(average)

    return render_template("profile.html", title="Profile", user=user, average=average)


@app.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    if request.method == 'POST':
        user_edit = User.query.get_or_404(current_user.id)
        try:
            user_edit.name = request.form['name']
            user_edit.icon = request.form['icon']
            user_edit.email = request.form['email']
            user_edit.department = request.form['department']
            user_edit.description = request.form['description']
            user_edit.hobbies = Hobby.query.filter(Hobby.id.in_(request.form.getlist('hobbies'))).all()
            db.session.add(user_edit)
            db.session.commit()
            return redirect(url_for('profile'))
        except Exception:
            db.session.rollback()
            flash("Edit fail", 'danger')
            return redirect(url_for('profile_edit'))

    user = current_user
    hobbies = Hobby.query.all()

    return render_template("edit_profile.html", title="Profile Edit", user=user, hobbies=hobbies)

@app.route('/search/users', methods=["GET", "POST"])
def search_users():
    if request.method == 'POST':
        search_word = request.form['query']
        search = "%{}%".format(search_word)
        users = User.query.filter(User.name.like(search)).filter(User.id != current_user.id).all()
    return render_template('components/user-home.html', users=[user.selialize() for user in users])

# @app.route("/chatroom/<int:room_name>&&<int:to_id>", methods=['GET', 'POST'])
@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if request.args.get('room'):
        session['room'] = request.args.get('room')
        
    return render_template("chat.html", title="Chat", session=session, current_user=current_user, to_user=request.args.get("user"))

@app.route("/wait_room", methods=['GET', 'POST'])
def request_chat():
    print(request.method)
    # session["room"] = request.args["room_name"]
    if request.method == "POST":
        
        session['room'] = request.form['RoomName']
        print("DEF REQUEST " + current_user.name + " have session below")
        print(session)

        data = {
            "room": session['room'],
            "from_id": current_user.id,
            "to_id": request.form['ToUserID'],
            "name": current_user.name,
        }
        Notice(data).save()
    return render_template("wait_room.html", title="Wait Room", session=session)

@app.route("/invite_room")
def process_invite_chat():
    user = request.args.get("user_id")
    room = request.args.get("room")
    content = request.args.get("content")
    print(room)
    return render_template("invite_chat.html", title= "Invite Room", room=room, content=content, user=user)

######################  CHAT  ####################################

@socket_app.on('join', namespace='/chat')
def join(message):
    print("Call packet JOIN")
    room = session.get('room')
    join_room(room)
    data = {
        "type":"JOIN",
        "from_user": current_user.name,
        "msg": current_user.name + ' has entered the room.'
    }
    emit('status', data, room=room)
   


@socket_app.on('text', namespace='/chat')
def text(message):
    print("RECEIVE NEW MESS")
    print(message)
    room = session.get('room')
    data = {
        "type": "CHAT",
        "from": current_user.name,
        "msg": message['msg']
    }
    print(data)
    emit('message', data, room=room)
    


@socket_app.on('left', namespace='/chat')
def left(data):
    room = session.get('room')
    leave_room(room)
    session.clear()
    print(session)
    data = {
        "type": "LEFT",
        'msg' : data['msg']
    }
    emit('status',data, room=room)

@socket_app.on('refuse', namespace="/wait")
def refuse(data):
    data = {
        'msg': "Your invitation refused"
    }
    emit('go_to_home', data, namespace="/wait",broadcast=True)

    # emit('refuse')
@socket_app.on('accept_invite', namespace="/wait")
def accept(data):
    print(data)
    # session['room'] = data["room"]
    # print("DEF ACCEPT " + current_user.name + " have session below")
    # print(session)
    # join_room(session['room'])
    # data = {
    #     "type":"JOIN",
    #     "from_user": current_user.name,
    #     "msg": current_user.name + ' has entered the room.'
    # }
    data = {
        ''
        'msg': "Your invitation accepted"
    }
    emit('go_to_chat', data, namespace="/wait",broadcast=True)

###########################################################
from app.seeds import create_data
@app.route("/seed")
def seed_data():
    create_data()
    return redirect('/')

@app.route('/review', methods=["GET", "POST"])
def review_result():
    to_user = request.args.get("to_user")
    print(to_user)

    if request.method == "POST":
        data = {
            "content": request.form['user_review'],
            "score": request.form['score'],
            "fk_user_from": current_user.id,
            "fk_user_to": to_user.id,
        }
        review = Review(data)
        try:
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception:
            db.session.rollback()
            flash("Edit fail", 'danger')
            return redirect(url_for('review_result'))

    user = current_user
    return render_template('review.html', user=user)

    
@app.route('/list-review', methods=["GET"])
def list_review():

    users_review = User.query\
    .filter(Review.fk_user_to == current_user.id)\
    .join(Review, User.id==Review.fk_user_from)\
    .add_columns(User.name, User.email, User.icon, Review.content, Review.score).all()
    return render_template('list_review.html', user=current_user, users_review=users_review)

@app.route('/profile/<name>')
def profile_detail(name): 

    user = User.query.filter(User.name==name).first()
    average = Review.query.with_entities(func.avg(Review.score).label('score')).filter(Review.fk_user_to == user.id).scalar()

    if average != None:
        average = round(average)

    return render_template("profile_detail.html", title="Profile", user=user, average=average)

@app.route('/list-review/<name>', methods=["GET"])
def list_review_member(name):
    user = User.query.filter(User.name==name).first()

    users_review = User.query\
    .filter(Review.fk_user_to == user.id)\
    .join(Review, User.id==Review.fk_user_from)\
    .add_columns(User.name, User.email, User.icon, Review.content, Review.score).all()
    return render_template('list_review.html', user=current_user, users_review=users_review)