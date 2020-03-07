from application import db

from flask import current_app
from flask import request, session, render_template, redirect, url_for, flash
from six.moves.urllib.parse import urlencode

from . import bp
from .session import Session
from .forms import LoginForm, RegistrationForm
from .models import DelegatedUser
from .services import Users
from .decorators import requires_auth

import json
from datetime import datetime

#  Callback
#  ----------------------------------------------------------------
@bp.route('/callback')
def callback():
    """ Auth0 callback
        - user profile extraction
        - session setup
    """
    # authorize connection:
    token = current_app.config['AUTH0'].authorize_access_token()
    # get user profile
    #
    # GET https://DOMAIN/userinfo
    # Authorization: 'Bearer {ACCESS_TOKEN}'
    # 
    response = current_app.config['AUTH0'].get('userinfo')
    userinfo = response.json()

    # set up session:
    _, id = userinfo['sub'].split('|')
    session[Session.ID] = id
    session[Session.TOKEN] = token
    session[Session.PROFILE] = {
        "nickname": userinfo["nickname"],
        "location": userinfo["user_metadata"]["location"] if ("user_metadata" in userinfo and "location" in userinfo["user_metadata"]) else "",
        "about_me": userinfo["user_metadata"]["about_me"] if ("user_metadata" in userinfo and "about_me" in userinfo["user_metadata"]) else "",
        "updated_at": userinfo["updated_at"],
        "last_login": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

    # prompt:
    flash('Welcome!')

    return redirect(url_for('main.index'))

#  Login
#  ----------------------------------------------------------------
@bp.route('/login', methods=['GET'])
def login():
    """ Auth0 login
    """
    return current_app.config['AUTH0'].authorize_redirect(
        redirect_uri='http://localhost:51080/auth/v2/callback'
    )

#  Register
#  ----------------------------------------------------------------
users = Users()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """ register new account
    """
    # init form:
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        # validate form:
        if form.validate():
            # create user in backend:
            response = users.post(
                email = form.email.data,
                password = form.password.data
            )
            # success:
            if 'identities' in response:         
                try:
                    # create user:
                    _, id = response['user_id'].split('|')
                    delegated_user = DelegatedUser(
                        id = id,
                        email = response['email'],
                        nickname = response['nickname']
                    )  
                    # insert:
                    db.session.add(delegated_user)
                    # write
                    db.session.commit()
                    # on successful registration, flash success
                    flash('New account was successfully created. You can login now.')
                    return redirect(url_for('.login'))
                except:
                    db.session.rollback()
                    # on unsuccessful registration, flash an error instead.
                    flash('An error occurred. New account could not be created.')
                finally:
                    db.session.close()
            # failure:
            else:
                flash(response['message'])
        else:
            # for debugging only:
            flash(form.errors)
        
    return render_template('auth/v2/forms/register.html', form=form)

#  Logout
#  ----------------------------------------------------------------
@bp.route('/logout', methods=['GET'])
@requires_auth
def logout():
    """ Auth0 logout
    """
    # clear session:
    session.clear()
    # prompt:
    flash('You have been logged out.')
    # build query params:
    query_params = {
        'returnTo': 'http://localhost:51080/', 
        'client_id': current_app.config['AUTH0_CLIENT_ID']
    }

    return redirect(
        current_app.config['AUTH0_LOGOUT_URL'] + '?' + urlencode(query_params)
    )
