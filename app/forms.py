from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Password Confirmation',
                                validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Sign up')


class ReviewForm(FlaskForm):
    userreview = StringField('user_review',)
    userscore = StringField('user_score',)  # DataRequiredはずっと入力するという処理になる

    submit = SubmitField('Review')

class ReviewResultForm(FlaskForm):
    userreview = StringField('user_review',)
    userscore = StringField('user_score',)  # DataRequiredはずっと入力するという処理になる
    scoreresult = StringField('scoreresult',) 

    submit = SubmitField('Review')