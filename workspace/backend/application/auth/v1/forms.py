from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

class LoginForm(FlaskForm):
    # account:
    email = StringField(
        'E-Mail', 
        validators = [
            DataRequired(), 
            Length(1, 64),
            Email()
        ]
    )
    # password:
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired()
        ]
    )
    # track:
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    # account:
    email = StringField(
        'E-Mail', 
        validators = [
            DataRequired(), 
            Length(1, 64),
            Email()
        ]
    )
    # username
    username = StringField(
        'Username', 
        validators = [
            DataRequired(), 
            Length(1, 64),
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'Usernames must have only letters, numbers, dots or underscores'
            )
        ]
    )
    # password:
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            EqualTo('password_confirmation', message='Passwords must match.')
        ]
    )
    password_confirmation = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired()
        ]
    )
