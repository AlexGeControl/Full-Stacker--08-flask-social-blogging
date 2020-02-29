from flask import render_template
from . import bp

@bp.route('/')
def index():
    """ welcome to identity and access management development!
    """

    return render_template('pages/home.html')