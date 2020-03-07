from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


class ProfileForm(Form):
    # nickname:
    nickname = StringField(
        'nickname', 
        validators = [
            DataRequired(),
            Length(1, 64)
        ]
    )
    # location:
    location = SelectField(
        'location', 
        validators = [
            DataRequired(),
            Length(1, 64)
        ],
        choices=[
            ('Shanghai China', 'Shanghai China'),
            ('Beijing China', 'Beijing China'),
            ('Shenzhen China', 'Shenzhen China'),
            ('Guangzhou China', 'Guangzhou China'),
            ('Suzhou China', 'Suzhou China'),
            ('Chengdu China', 'Chengdu China'),
        ]
    )
    # about_me:
    about_me = TextAreaField(
        'about_me',
        validators = [
            Optional(),
            Length(0, 140)
        ]
    )
