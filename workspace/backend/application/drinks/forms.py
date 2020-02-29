from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class DrinkForm(FlaskForm):
    # account:
    title = StringField(
        'Title', 
        validators = [
            DataRequired(), 
            Length(1, 80)
        ]
    )
    # recipe:
    recipe = SelectMultipleField(
        'Recipe', 
        validators = [
            DataRequired()
        ],
        choices=[
            ('foam', 'Foam'),
            ('milk', 'Milk'),
            ('coffee', 'Coffe'),
            ('matcha', 'Matcha'),
        ]
    )
