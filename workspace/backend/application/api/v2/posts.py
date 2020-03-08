from application import db

from application.auth.v2.models import DelegatedUser
from application.models import Post

from flask import current_app
from flask import request

from flask_restplus import Namespace, Resource, fields

# create namespace
ns = Namespace('posts', description='Posts') 

# create response marshallings:
post_brief = ns.model('PostBrief', 
    {
        'id': fields.String(readonly=True, description='The post unique identifier'),
        'title': fields.String(required=True, description='The post title'),
        'author': fields.String(required=True, description='The post author'),
        'timestamp': fields.DateTime(required=True, description='The post creation time')
    }
)

@ns.route('/')
class PostList(Resource):
    ''' posts
        - GET a list of all posts
        - POST to add new tasks
    '''
    @ns.doc('list_todos')
    @ns.marshal_list_with(post_brief)
    def get(self):
        '''List all posts
        '''
        # parse query parameter page:
        page = request.args.get('page', 1, type=int)

        # data:
        user_subq = DelegatedUser.query.with_entities(
            DelegatedUser.id,
            DelegatedUser.nickname
        ).subquery()

        # generate pagination:
        pagination = Post.query.with_entities(
            Post.uuid,
            Post.title,
            user_subq.c.nickname.label("author"),
            Post.timestamp
        ).join(
            user_subq, Post.author_id == user_subq.c.id
        ).order_by(
            Post.timestamp.desc()
        ).paginate(
            page, per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
        posts = pagination.items

        # format:
        posts=[
            {
                "id": id.hex,
                "title": title,
                "author": author,
                "timestamp": timestamp,
            } for (id, title, author, timestamp) in posts
        ]

        return posts
