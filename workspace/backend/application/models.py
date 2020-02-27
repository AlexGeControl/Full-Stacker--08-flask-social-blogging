from application import db

import factory
import factory.fuzzy

import random
import json

#----------------------------------------------------------------------------#
# model
#----------------------------------------------------------------------------#
class Drink(db.Model):
    # follow the best practice
    __tablename__ = 'drinks'

    # primary key, auto-increasing
    id = db.Column(db.Integer(), primary_key=True)

    # title
    title = db.Column(db.String(80), unique=True)
    
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return json.dumps(self.short())


    def short(self):
        ''' short form representation, without details, of the Drink model
        '''
        short_recipe = [
            {
                'color': r['color'], 
                'parts': r['parts']
            } for r in json.loads(self.recipe)
        ]

        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }


    def long(self):
        ''' long form representation, with full details, of the Drink model
        '''

        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

#----------------------------------------------------------------------------#
# data generator
#----------------------------------------------------------------------------#
class Ingredient(object):
    def __init__(self, name, color, parts):
        self.name = name
        self.color = color
        self.parts = parts

    def to_json(self):
        data = {
            "name": self.name,
            "color": self.color,
            "parts": self.parts
        }

        return data


class IngredientFactory(factory.Factory):
    class Meta:
        model = Ingredient

    name = factory.Iterator(
        [
            'milk', 
            'foam', 
            'coffee', 
            'matcha'
        ], cycle=True
    )
    color = factory.Iterator(
        [
            'grey', 
            'white', 
            'brown',
            'green'
        ], cycle=True
    )
    # parts should be random int from [1, 3]:
    parts = factory.fuzzy.FuzzyInteger(1, 3)


class DrinkFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ test drink generator
    """
    class Meta:
        model = Drink
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)

    title = factory.fuzzy.FuzzyText(length=12)

    @factory.sequence
    def recipe(n):
        # init generator:
        random.seed(n)
        # decide the num. of ingredients:
        num_ingredients = random.randint(1, 3)

        data = [
            IngredientFactory().to_json() for _ in range(num_ingredients)
        ]

        return json.dumps(data)

