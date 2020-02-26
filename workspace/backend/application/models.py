from application import db
import factory

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Question(db.Model):
  """ table questions
  """
  # follow the best practice
  __tablename__ = 'questions'
  
  # primary key:
  id = db.Column(db.Integer, primary_key=True)

  # attributes:
  question = db.Column(db.Text, nullable=False)
  answer = db.Column(db.Text, nullable=False)
  difficulty = db.Column(db.Integer, nullable=False)

  # relationship
  category_id = db.Column(
    db.Integer, 
    db.ForeignKey(
      'categories.id', 
      onupdate='CASCADE', ondelete='SET NULL'
    ), 
    nullable=True
  )

  def __repr__(self):
    return f'<Question id="{self.id}" question="{self.question}" answer="{self.answer}" difficulty="{self.difficulty}" category_id="{self.category_id}">'

  def to_json(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'difficulty': self.difficulty,
      'category_id': self.category_id
    }
  
  def from_json(self, json):
    self.question = json['question'] 
    self.answer = json['answer'] 
    self.difficulty = int(json['difficulty'])
    self.category_id = int(json['category_id']) 


class QuestionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ test question generator
    """
    class Meta:
        model = Question
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)

    question = factory.Sequence(lambda n: "Question {}".format(n))
    answer = factory.Sequence(lambda n: "Answer {}".format(n))
    difficulty = factory.Iterator([1, 2, 3, 4, 5], cycle=True)

    category_id = factory.Sequence(lambda n: n)


class Category(db.Model):
  """ table questions
  """
  # follow the best practice  
  __tablename__ = 'categories'
  
  # primary key:
  id = db.Column(db.Integer, primary_key=True)

  # attributes:
  type = db.Column(db.Text, nullable=False)

  # relationship:
  questions = db.relationship('Question', backref='category', lazy=True)

  def __repr__(self):
    return f'<Category id="{self.id}" type="{self.type}">'

  def to_json(self):
    return {
      'id': self.id,
      'type': self.type
    }

  def from_json(self, json):
    self.type = json['type'] 


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ test category generator
    """
    class Meta:
        model = Category
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)

    type = factory.Sequence(lambda n: "Category {}".format(n))