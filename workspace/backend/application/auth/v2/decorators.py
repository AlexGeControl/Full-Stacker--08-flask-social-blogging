from functools import wraps
from flask import session, redirect, url_for, abort
from .session import Session


def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if Session.PROFILE not in session:
            return redirect(url_for('auth_v2.login'))
        return f(*args, **kwargs)
    return decorated_function