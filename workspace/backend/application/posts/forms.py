from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    # title:
    title = StringField(
        'Title', 
        validators = [
            DataRequired()
        ]
    )
    # contents:
    contents = TextAreaField(
        'Contents',
        validators = [
            DataRequired()
        ]
    )
