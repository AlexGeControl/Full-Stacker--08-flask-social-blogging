from application import db
from application.auth.models import Role, User

from flask import render_template, redirect, request, url_for, flash

from . import bp
from .forms import LoginForm
from application.utils import convert_form_dict_to_dict

from flask_login import login_user
from flask_login import logout_user, login_required

#  Login
#  ----------------------------------------------------------------
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """ render login form
    """
    # init form:
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # get user:
        user = User.query.filter(
            User.email == form.email.data
        ).first()        
        
        # verify:
        if (not user is None) and (user.verify_password(form.password.data)):
            # record user as logged in in the user session if remember me is checked:            
            login_user(user, form.remember_me.data)
            # parse target URL from query argument next            
            next = request.args.get('next')
            # if target URL is not given or not a relative one, redirect to main            
            if next is None or not next.startswith('/'):               
                next = url_for('main.index')
            # head to target URL:
            return redirect(next)
        
        # login failure prompt:
        flash('Invalid username or password. Please try again.')
    else:
        # for debugging only:
        # flash(form.errors)
    return render_template('auth/forms/login.html', form=form)

#  Register
#  ----------------------------------------------------------------
@bp.route('/register', methods=['GET', 'POST'])
def register():
    pass

#  Logout
#  ----------------------------------------------------------------
@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """ logout
    """
    logout_user()
    flash('You have been logged out.')

    return redirect(url_for('main.index'))
