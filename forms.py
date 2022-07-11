from email import message
from logging.config import valid_ident
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


class RegisterUserForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired(), Length(
        max=20, message='Username cannot be longer than 20 characters')])

    password = PasswordField('Password', validators=[InputRequired()])

    email = StringField('Email', validators=[InputRequired(), Length(
        max=50, message='Email cannot be longer than 50 characters'), Email(message='Please enter a valid email address')])

    first_name = StringField('First Name', validators=[InputRequired(), Length(
        max=30, message='First Name cannot be longer than 30 characters')])

    last_name = StringField('last Name', validators=[InputRequired(), Length(
        max=30, message='Last Name cannot be longer than 30 characters')])


class LoginUserForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])

    password = PasswordField('Password', validators=[InputRequired()])


class FeedbackForm(FlaskForm):

    title = StringField('Title', validators=[InputRequired(), Length(
        max=100, message='Title cannot be longer than 100 characters')])

    content = TextAreaField('Content', validators=[InputRequired()])
