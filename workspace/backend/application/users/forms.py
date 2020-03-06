from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    # title:
    title = StringField(
        'Title', 
        validators = [
            DataRequired()
        ]
    )
    # contents -- using markdown rich text editor from PageDown:
    contents = PageDownField(
        'Contents',
        validators = [
            DataRequired()
        ]
    )
