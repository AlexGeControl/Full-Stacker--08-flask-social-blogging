from application import db
from application.auth.models import Role, User

from flask import render_template, redirect, request, url_for, flash

from . import bp
from .forms import LoginForm
from application.utils import convert_form_dict_to_dict

from flask_login import login_user
from flask_login import logout_user, login_required

@bp.route('/login', methods=['GET'])
def login():
    """ render login form
    """
    # create empty form:
    form = LoginForm()

    return render_template('auth/forms/login.html', form=form)

@bp.route('/login', methods=['POST'])
def login_submission():
    """ verify login
    """
    # parse POSTed form:
    account= convert_form_dict_to_dict(request.form)
    
    # get user:
    user = User.query.filter(
        User.email == account["email"]
    ).first()        
    
    # verify:
    if (user is None) or (not user.verify_password(account["password"])):
        flash('Invalid username or password. Please try again.')

    # record user as logged in in the user session if remember me is checked:            
    login_user(user, account["remember_me"])
    # parse target URL from query argument next            
    next = request.args.get('next')
    # if target URL is not given or not a relative one, redirect to main            
    if next is None or not next.startswith('/'):                
        next = url_for('main.index')

    return redirect(next)

@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """ logout
    """
    logout_user()
    flash('You have been logged out.')

    return redirect(url_for('main.index'))
