from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    # account:
    email = StringField(
        'email', 
        validators = [
            DataRequired(), 
            Length(1, 64),
            Email()
        ]
    )
    # password:
    password = PasswordField(
        'password', 
        validators=[
            DataRequired()
        ]
    )
    # track
    remember_me = BooleanField('remember_me')