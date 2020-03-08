from application import db

from application.auth.v2.models import DelegatedUser
from application.models import Post

from flask import current_app
from flask import abort, request

from flask_restplus import Namespace, Resource, fields

from datetime import datetime
import uuid

# create namespace
ns = Namespace('posts', description='Posts') 

# create response schemas:
post_brief = ns.model('PostBrief', 
    {
        'id': fields.String(readonly=True, description='The post unique identifier'),
        'title': fields.String(required=True, description='The post title'),
        'author': fields.String(required=True, description='The post author'),
        'timestamp': fields.DateTime(required=True, description='The post creation time')
    }
)

post_detail = ns.model('PostDetail', 
    {
        'id': fields.String(readonly=True, description='The post unique identifier'),
        'title': fields.String(required=True, description='The post title'),
        'contents': fields.String(required=True, description='The post contents'),
        'author_id': fields.String(readonly=True, description='The author unique identifier'),
        'timestamp': fields.DateTime(required=True, description='The post creation time')
    }
)

post_input = ns.model('PostInput', 
    {
        'title': fields.String(required=True, description='The to-be-created post title'),
        'contents': fields.String(required=True, description='The to-be-created post contents')
    }
)

@ns.route('/')
class PostList(Resource):
    ''' post list
        - GET a list of all posts
        - POST to add new tasks
    '''
    @ns.doc(
        'list_todos', 
        params={'page': 'Page number for pagination'}
    )
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
            user_subq.c.nickname.label('author'),
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
    
    @ns.doc('create_todo')
    @ns.expect(post_input)
    @ns.response(201, 'Post created')
    @ns.marshal_with(post_detail, code=201)
    @ns.response(500, 'Internal error. Post could not be deleted')
    def post(self):
        '''Create a new post
        '''
        # parse input post:
        post_new = request.get_json()

        error = True
        try:
            # create new post:
            id = Post.query.count() + 1

            post = Post(
                id = id,
                title = post_new['title'],
                contents = post_new['contents'],
                # TODO: parse author_id from JWT payload, currently fixed to admin01
                author_id = '5e6305a010b4610d3d895cd4'
            )
            # insert:
            db.session.add(post)
            # write
            db.session.commit()
            # prepare response:
            post_created = post.to_json()
            post_created['timestamp'] = datetime.strptime(post_created['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            # update flag:
            error = False
        except:
            # rollback:
            db.session.rollback()
            # update flag:
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, description="An error occurred. Post could not be created.")

        return post_created, 201

@ns.route('/<id>')
@ns.param('id', 'The post unique identifier')
class PostInstance(Resource):
    ''' post instance
    '''
    @ns.doc('get_post')
    @ns.marshal_with(post_detail)
    @ns.response(404, 'Post not found')
    def get(self, id):
        '''Fetch a given post
        '''
        # data:
        post = Post.query.with_entities(
            Post.uuid,
            Post.title,
            Post.contents,
            Post.timestamp,
            Post.author_id
        ).filter(
            Post.uuid == uuid.UUID(id)
        ).first()

        if post is None:
            abort(
                404, 
                description='There is no post with id={}'.format(id)
            )

        # format:
        post = {
            "id": post.uuid.hex,
            "title": post.title,
            "author_id": post.author_id,
            "timestamp": post.timestamp,
            "contents": post.contents
        }

        return post

    @ns.expect(post_input)
    @ns.marshal_with(post_detail)
    @ns.response(404, 'Post not found')
    @ns.response(500, 'Internal error. Post could not be deleted')
    def patch(self, id):
        '''Update a given post
        '''
        # parse input post:
        post_updated = request.get_json()

        error = True

        try:
            # select:
            post = Post.query.filter(
                Post.uuid == uuid.UUID(id)
            ).first()
            
            if post is None:
                abort(
                    404, 
                    description='There is no post with id={}'.format(id)
                )
            # update:
            post.title = post_updated["title"]
            post.contents = post_updated["contents"]
            # insert:
            db.session.add(post)
            # write
            db.session.commit()
            # prepare response:
            post_updated = post.to_json()
            post_updated['timestamp'] = datetime.strptime(post_updated['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            # update flag:
            error = False
        except:
            # rollback:
            db.session.rollback()
            # update flag:
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, description="An error occurred. Post could not be updated.")

        return post_updated


    @ns.doc('delete_post')
    @ns.response(204, 'Post deleted')
    @ns.response(404, 'Post not found')
    @ns.response(500, 'Internal error. Post could not be deleted')
    def delete(self, id):
        '''Delete a given post
        '''
        error = True

        try:
            # select:
            post = Post.query.filter(
                Post.uuid == uuid.UUID(id)
            ).first()
            
            if post is None:
                abort(
                    404, 
                    description='There is no post with id={}'.format(id)
                )
            # delete:
            db.session.delete(post)
            db.session.commit()
            # update flag:
            error = False
        except:
            # rollback:
            db.session.rollback()
            # update flag:
            error = True
        finally:
            db.session.close()

        if error:
            abort(
                500, 
                description="An error occurred. Post with id={} could not be deleted.".format(id)
            )

        return '', 204
