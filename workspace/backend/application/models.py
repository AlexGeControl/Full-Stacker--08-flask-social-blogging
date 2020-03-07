from application import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

import factory
import factory.fuzzy
from faker import Faker

from datetime import datetime, timezone
import random
import json

# markdown rich text editor:
from markdown import markdown
import bleach

fake = Faker()

#----------------------------------------------------------------------------#
# posts
#----------------------------------------------------------------------------#
class Post(db.Model):
    # follow the best practice
    __tablename__ = 'posts'    
    
    # primary key:
    id = db.Column(db.Integer, primary_key=True)    
    
    # for public exposure:
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)

    # post info:
    title = db.Column(db.Text, nullable=False)
    contents = db.Column(db.Text, nullable=False)
    contents_html = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())    
    
    # relationship with users -- many-to-one
    author_id = db.Column(db.String(64), db.ForeignKey('delegated_users.id'))    

    # triggers:
    @staticmethod
    def on_contents_set(target, value, old_value, initiator):
        """ on contents set hook
        """
        # html tag whitelist:
        allowed_tags = [
            'a', 
            'abbr', 
            'acronym', 
            'b', 
            'blockquote', 
            'code',
            'em', 
            'i', 
            'li', 
            'ol', 
            'pre', 
            'strong', 
            'ul',
            'h1', 'h2', 'h3', 
            'p'
        ]
        target.contents_html = bleach.linkify(
            bleach.clean(
                markdown(value, output_format='html'),
                tags=allowed_tags, 
                strip=True
            )
        )

    def _format_timestamp_default(self):
        """ format timestamp
        """
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def _format_timestamp_iso(self):
        """ format timestamp into iso
        """
        return self.timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def __repr__(self):
        return f'<Post id="{self.id}" datetime="{self._format_timestamp_default()}" title="{self.title}">'

    def to_json(self):
        """ format as python dict
        """
        data = {
            "id": self.uuid.hex,
            "title": self.title,
            "contents": self.contents,
            "timestamp": self._format_timestamp_iso(),
            "author_id": self.author_id,
        }

        return data

    def from_json(self, data):
        """ update object using json input
        """
        self.title = data.get('title', '')
        self.contents = data.get('contents', '')
        self.timestamp = datetime.utcnow() if (not 'timestamp' in data) else \
            datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")

# triggers:
db.event.listen(Post.contents, 'set', Post.on_contents_set)

# fake data generator:
class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ test post generator
    """
    class Meta:
        model = Post
        sqlalchemy_session = db.session

    # id should start from 1:
    id = factory.Sequence(lambda n: n + 1)

    # use faker API to generate better test data:
    title = factory.Faker('sentence', nb_words=4)
    contents = factory.Faker('text')
    timestamp = factory.fuzzy.FuzzyDateTime(datetime(2018, 1, 1, tzinfo=timezone.utc))

    author_id = factory.Sequence(lambda n: uuid4().hex)

#----------------------------------------------------------------------------#
# follows
#----------------------------------------------------------------------------#
class Follow(db.Model):
    # follow the best practice
    __tablename__ = 'follows' 

    # primary key:
    id = db.Column(db.Integer, primary_key=True) 

    # relationships:
    follower_id = db.Column(db.String(64), db.ForeignKey('delegated_users.id')) 
    followed_id = db.Column(db.String(64), db.ForeignKey('delegated_users.id')) 

    # attributes:
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow()) 

