from application import db
from application.auth.v2.models import DelegatedUser
from application.auth.v2.decorators import requires_auth

from flask import current_app
from flask import session
from application.auth.v2.session import Session
from flask import flash, request, render_template, redirect, url_for

from . import bp

@bp.route('/follow/<user_id>', methods=['GET'])
@requires_auth
def follow(user_id):
    """ let current user follow given user
    """
    # get user:
    user = DelegatedUser.query.get_or_404(
        user_id, 
        description='There is no user with id={}'.format(user_id) 
    )

    # get current user:
    current_user = DelegatedUser.query.get(
        session[Session.ID]
    )

    # check follow:
    if current_user.is_following(user):
        flash('You are already following this user.')
    else:
        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {user.nickname}.')

    return redirect(url_for('users.show_user', user_id=user_id))

@bp.route('/unfollow/<user_id>', methods=['GET'])
@requires_auth
def unfollow(user_id):
    """ let current user unfollow given user
    """
    # get user:
    user = DelegatedUser.query.get_or_404(
        user_id, 
        description='There is no user with id={}'.format(user_id) 
    )

    # get current user:
    current_user = DelegatedUser.query.get(
        session[Session.ID]
    )

    # check follow:
    if not current_user.is_following(user):
        flash('You are currently not following this user.')
    else:
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are now not following {user.nickname}.')

    return redirect(url_for('users.show_user', user_id=user_id))

@bp.route('/followers/<user_id>', methods=['GET'])
@requires_auth
def followers(user_id):
    """ get followers of given user
    """
    # get user:
    user = DelegatedUser.query.get_or_404(
        user_id, 
        description='There is no user with id={}'.format(user_id) 
    )

    # parse query parameter page:
    page = request.args.get('page', 1, type=int)

    # generate pagination:
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FOLLOWS_PER_PAGE'],
        error_out=False
    )
    
    # format:
    follows = pagination.items
    follows=[
        {
            "user": follow.follower,
            "timestamp": follow.timestamp,
        } for follow in follows
    ]
    
    return render_template('follows/pages/followers.html', user=user, follows=follows, pagination=pagination)

@bp.route('/followed/<user_id>', methods=['GET'])
@requires_auth
def followed(user_id):
    """ get followers of given user
    """
    # get user:
    user = DelegatedUser.query.get_or_404(
        user_id, 
        description='There is no user with id={}'.format(user_id) 
    )

    # parse query parameter page:
    page = request.args.get('page', 1, type=int)

    # generate pagination:
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FOLLOWS_PER_PAGE'],
        error_out=False
    )
    
    # format:
    follows = pagination.items
    follows=[
        {
            "user": follow.followed,
            "timestamp": follow.timestamp,
        } for follow in follows
    ]
    
    return render_template('follows/pages/followed.html', user=user, follows=follows, pagination=pagination)
