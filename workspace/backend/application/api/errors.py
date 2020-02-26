from flask import jsonify

from . import bp

@bp.app_errorhandler(400)
def bad_request(error):
    # body:
    response = jsonify(
        {
            "success": False, 
            "error": 400,
            "message": str(error)
        }
    )

    return response, 400

@bp.app_errorhandler(404)
def not_found(error):
    # body:
    response = jsonify(
        {
            "success": False, 
            "error": 404,
            "message": str(error)
        }
    )

    return response, 404

@bp.app_errorhandler(500)
def internal_server_error(error):
    # body:
    response = jsonify(
        {
            "success": False, 
            "error": 500,
            "message": str(error)
        }
    )

    return response, 500