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
        'email', 
        validators = [
            DataRequired(), 
            Length(1, 64),
            Email()
        ]
    )
