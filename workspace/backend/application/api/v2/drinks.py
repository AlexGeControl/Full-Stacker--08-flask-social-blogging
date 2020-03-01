from application import db
from application.models import Drink

import json
from flask import abort, request, jsonify

from . import bp

from .auth.decorators import Permission, requires_auth

#  CREATE
#  ----------------------------------------------------------------
@bp.route('/drinks', methods=['POST'])
@requires_auth(permission = Permission.POST_DRINKS)
def create_drink(account_info):
    """
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    
    return
        status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
    """
    # parse POSTed json:
    drink_created = request.get_json()
    # serialize recipe as one string:
    drink_created["recipe"] = json.dumps(drink_created["recipe"])

    error = True
    try:
        drink = Drink(
            id = Drink.query.count() + 1,
            title = drink_created["title"],
            recipe = drink_created["recipe"]
        )
        # insert:
        db.session.add(drink)
        db.session.commit()
        error = False
        # prepare response:
        drink = drink.long()
    except:
        # rollback:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500, description="Failed to create new Drink")

    # format:
    response = jsonify(
        {
            "success": True,
            "drinks": [drink] 
        }
    )
    return response, 200

#  READ
#  ----------------------------------------------------------------
@bp.route('/drinks', methods=['GET'])
def get_drinks():
    """
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation

    return
        status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    error = True
    try:
        # select all drinks:
        drinks = Drink.query.all()
        error = False
    except:
        error = True
    finally:
        db.session.close()

    if error:
        abort(500, description="Failed to load drinks")

    # format:
    response = jsonify(
        {
            "success": True, 
            "drinks": [drink.short() for drink in drinks],
        }
    )

    return response, 200

@bp.route('/drinks-detail', methods=['GET'])
@requires_auth(permission = Permission.GET_DRINKS_DETAIL)
def get_drinks_detail(account_info):
    """
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation

    return 
        status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    error = True
    try:
        # select all drinks:
        drinks = Drink.query.all()
        error = False
    except:
        error = True
    finally:
        db.session.close()

    if error:
        abort(500, description="Failed to load drinks")

    # format:
    response = jsonify(
        {
            "success": True, 
            "drinks": [drink.long() for drink in drinks],
        }
    )

    return response, 200

#  PATCH
#  ----------------------------------------------------------------
@bp.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission = Permission.PATCH_DRINKS)
def edit_drink(account_info, id):
    """
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    
    return 
        status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    """
    # parse POSTed json:
    drink_edited = request.get_json()
    # serialize recipe as one string:
    drink_edited["recipe"] = json.dumps(drink_edited["recipe"])

    error = True
    try:
        # select:
        drink = Drink.query.get(id)
        # if resource is not found:
        if drink is None:
            abort(404, description="Drink with id={} not found".format(id))
        # update:
        drink.title = drink_edited["title"]
        drink.recipe = drink_edited["recipe"]
        # insert:
        db.session.add(drink)
        db.session.commit()
        error = False
        # prepare response:
        drink = drink.long()
    except:
        # rollback:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500, description="Failed to edit the Drink with id={}".format(id))

    # format:
    response = jsonify(
        {
            "success": True,
            "drinks": [drink] 
        }
    )
    return response, 200

#  DELETE
#  ----------------------------------------------------------------
@bp.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission = Permission.DELETE_DRINKS)
def delete_drink(account_info, id):
    """
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission

    return 
        status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    """
    error = True

    try:
        # select:
        drink = Drink.query.get(id)

        # if resource is not found:
        if drink is None:
            abort(404, description="Drink with id={} not found".format(id))

        # delete:
        db.session.delete(drink)
        db.session.commit()

        error = False
    except:
        # rollback:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500, description="Failed to delete Drink with id={}".format(id))
    
    # format:
    response = jsonify(
        {
            "success": True,
            "delete": id 
        }
    )

    return response, 200