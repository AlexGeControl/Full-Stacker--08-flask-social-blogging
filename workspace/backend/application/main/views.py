from flask import jsonify
from . import bp

@bp.route('/')
def index():
    """ welcome to identity and access management development!
    """
    response = jsonify(
        {'message':'Hello, Identity and Access Management development!'}
    )
    
    return response, 200