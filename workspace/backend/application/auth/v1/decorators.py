from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_drinks_detail_required(f):
    return permission_required(Permission.GET_DRINKS_DETAIL)(f)

def post_drinks_required(f):
    return permission_required(Permission.POST_DRINKS)(f)

def patch_drinks_required(f):
    return permission_required(Permission.PATCH_DRINKS)(f)

def delete_drinks_required(f):
    return permission_required(Permission.DELETE_DRINKS)(f)

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)