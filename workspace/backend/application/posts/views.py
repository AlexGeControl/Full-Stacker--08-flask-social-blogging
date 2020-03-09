from application import db
import uuid
from application.auth.v2.models import DelegatedUser
from application.models import Post

from flask import current_app
from flask import session
from application.auth.v2.session import Session
from flask import abort, request, flash, render_template, redirect, url_for
# auth v2:
from application.auth.v2.decorators import requires_auth

from . import bp

from .forms import PostForm

from datetime import datetime

#  CREATE
#  ----------------------------------------------------------------
@bp.route('/create', methods=['GET', 'POST'])
@requires_auth
def create_post():
    """ render empty form for new post creation
    """
    if request.method == 'GET':
        # create empty form:
        form = PostForm()
    if request.method == 'POST': 
        # init form with POSTed form:
        form = PostForm(request.form)

        if form.validate():        
            try:
                # create new post id:
                if Post.query.count() == 0:
                    id = 1
                else:
                    from sqlalchemy.sql import func
                    post_id_summary = db.session.query(
                        func.max(Post.id).label("max")
                    ).one()
                    id = post_id_summary.max + 1
                
                # create new post:
                post = Post(
                    id = id,
                    title = form.title.data,
                    contents = form.contents.data,
                    author_id = session[Session.ID]
                )
                # insert:
                db.session.add(post)
                # commit:
                db.session.commit()
                
                # on successful registration, flash success
                flash('Post was successfully created.')
                return redirect(url_for('posts.posts'))
            except:
                db.session.rollback()
                # on unsuccessful registration, flash an error instead.
                flash('An error occurred. Post could not be created.')
            finally:
                db.session.close()
        else:
            # for debugging only:
            flash(form.errors)
            pass
            
    return render_template('posts/forms/post.html', form=form)

#  READ
#  ----------------------------------------------------------------
@bp.route('/', methods=['GET'])
def posts():
    """ show all posts
    """
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
    
    return render_template('posts/pages/posts.html', posts=posts, pagination=pagination)

@bp.route('/<post_uuid>')
@requires_auth
def show_post(post_uuid):
    """ show given post
    """
    # data:
    user_subq = DelegatedUser.query.with_entities(
        DelegatedUser.id,
        DelegatedUser.nickname
    ).subquery()

    post = Post.query.with_entities(
        Post.uuid,
        Post.title,
        user_subq.c.nickname.label("author"),
        Post.timestamp,
        Post.contents,
        Post.contents_html
    ).filter(
        Post.uuid == uuid.UUID(post_uuid)
    ).join(
        user_subq, Post.author_id == user_subq.c.id
    ).first()

    if post is None:
        abort(
            404, 
            description='There is no post with id={}'.format(post_uuid)
        )

    post = {
        "id": post.uuid.hex,
        "title": post.title,
        "author": post.author,
        "timestamp": post.timestamp,
        "contents": post.contents,
        "contents_html": post.contents_html
    }

    return render_template('posts/pages/post.html', post=post)

#  UPDATE
#  ----------------------------------------------------------------
@bp.route('/<post_uuid>/edit', methods=['GET', 'POST'])
@requires_auth
def edit_post(post_uuid):
    """ render form pre-filled with given post
    """
    # select post:
    post = Post.query.filter(
        Post.uuid == uuid.UUID(post_uuid)
    ).first_or_404(
        description='There is no post with id={}'.format(post_uuid)
    )

    if request.method == 'GET':
        # init form with selected post:
        post = post.to_json()
        form = PostForm(
            title = post["title"], 
            contents = post["contents"]
        )
    if request.method == 'POST': 
        # init form with POSTed form:
        form = PostForm(request.form)

        if form.validate():        
            try:
                # update post:
                post.title = form.title.data
                post.contents = form.contents.data
                post.timestamp = datetime.utcnow()
                # insert:
                db.session.add(post)
                # write
                db.session.commit()
                # on successful registration, flash success
                flash('Post was successfully updated.')
                return redirect(url_for('posts.posts'))
            except:
                db.session.rollback()
                # on unsuccessful registration, flash an error instead.
                flash('An error occurred. Post could not be updated.')
            finally:
                db.session.close()
        else:
            # for debugging only:
            flash(form.errors)
            pass
            
    return render_template('posts/forms/post.html', form=form, post=post)

#  DELETE
#  ----------------------------------------------------------------
@bp.route('/<post_uuid>', methods=['DELETE'])
@requires_auth
def delete_post(post_uuid):
    """ delete post
    """
    error = True

    try:
        # find:
        post = Post.query.filter(
            Post.uuid == uuid.UUID(post_uuid)
        ).first_or_404(
            description='There is no post with id={}'.format(post_uuid)
        )
        db.session.delete(post)
        # write
        db.session.commit()
        # on successful db insert, flash success
        flash('Post was successfully deleted!')
        error = False
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Post could not be deleted.')
        error = True
    finally:
        db.session.close()

    if error:
        abort(400)

    return redirect(url_for('posts.posts'))
