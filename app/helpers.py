from collections import defaultdict
import re
import bcrypt

from app.models import *
import random
from app import db

def generate_hash(password):
    # return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed    

def best_susume_user():

    pass

def the_most_setsuzoku_user(user_id):

    reviews = Review.query.order_by(Review.score).filter_by(fk_user_from=user_id).all()

    occurs = defaultdict(int)
    for review in reviews:
        occurs[review.fk_user_to] += 1
    users = User.query.filter(User.id.in_(occurs.keys())).all()
    users = list(sorted(users, key=lambda x: occurs[x.id], reverse=True))
    # select reviews.fk_user_to, count(*) from reviews
    # where reviews.fk_user_from = 3
    # group by reviews.fk_user_to
    # order by count(*) DESC;
    
    return [(user, occurs[user.id]) for user in users]

def last_setsuzoku_user(user_id):
    review_users = db.session.query(User, Review).order_by(Review.created_at.desc()).filter(Review.fk_user_from==user_id).join(User, User.id==Review.fk_user_to).limit(5).all()
    print(review_users)    
    return set([(user[0], user[1].created_at.strftime('%a, %d %b %Y %X %p')) for user in review_users])
    return users

