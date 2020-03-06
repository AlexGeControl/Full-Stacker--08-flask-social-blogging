from datetime import datetime

from application import db
from application.auth.v2.models import DelegatedUser

from flask import current_app
from flask import abort, request, flash, render_template, redirect, url_for

from . import bp
from application.auth.v2.services import UserByEmail

#  READ
#  ----------------------------------------------------------------
user_by_email = UserByEmail()

@bp.route('/<id>')
def show_user(id):
    """ show user profile
    """
    # data:
    user = DelegatedUser.query.with_entities(
        DelegatedUser.email,
    ).filter(
        DelegatedUser.id == id
    ).first_or_404(
        description='There is no user with id={}'.format(id)
    )

    # format:
    (email, ) = user

    user = user_by_email.get(email)[0]

    user = {
        "id": id,
        "nickname": user["nickname"],
        "about_me": "Coming Soon. Stay Tuned!",
        "location": "Shanghai, China",
        "last_updated": datetime.strptime(user["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        "last_seen": datetime.strptime(user["last_login"], "%Y-%m-%dT%H:%M:%S.%fZ")
    }

    return render_template('users/pages/user.html', user=user)
