from application import db
from application.models import Question, Category

from flask import current_app
from flask import request, abort, jsonify

from . import bp


#  CREATE
#  ----------------------------------------------------------------
@bp.route('/questions/', methods=['POST'])
def create_question():
    """ create new question using POSTed json
    """
    # parse POSTed json:
    question_created = request.get_json()
    error = True

    try:
        question = Question(**question_created)
        # insert:
        db.session.add(question)
        db.session.commit()
        error = False
    except:
        # rollback:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500, description="Failed to create new Question")

    # format:
    response = jsonify(
        {
            "success": True 
        }
    )
    return response, 201


#  READ
#  ----------------------------------------------------------------
@bp.route('/questions/', methods=['GET'])
def get_questions():
    """ GET all questions including pagination
    """
    # parse query argument page:
    page = request.args.get('page', 1, type=int)
    # create pagination:
    pagination = Question.query.order_by(
        Question.id
    ).paginate(
        page, per_page=current_app.config['FLASK_QUESTIONS_PER_PAGE'],
        error_out=False
    )
    # parse current questions & total count:
    questions = pagination.items
    total_questions = pagination.total
    # select all categories:
    categories = {
        _id: _type for (_id, _type) in Category.query.with_entities(
            Category.id,
            Category.type
        ).all()
    }

    # format:
    response = jsonify(
        {
            "questions": [question.to_json() for question in questions],
            "total_questions": total_questions,
            "categories": categories, 
            # TODO: implement current_category
            "current_category": None
        }
    )
    return response, 200

@bp.route('/questions/search/', methods=['POST'])
def search_questions():
    """ GET all questions with the search term in question body
    """
    # parse keyword:
    search_term = request.get_json().get("searchTerm", None)

    if search_term is None:
        abort(400, description="'searchTerm' not found".format())

    # select questions:
    questions = Question.query.filter(
        Question.question.contains(search_term)
    ).all()

    # format:
    response = jsonify(
        {
            "questions": [question.to_json() for question in questions],
            "total_questions": len(questions),
            # TODO: implement current_category
            "current_category": None
        }
    )

    return response, 200

@bp.route('/questions/<int:id>', methods=['GET'])
def get_question(id):
    """ GET question
    """
    # select:
    question = Question.query.get(id)

    # if resource is not found:
    if question is None:
        abort(404, description="Question with id={} not found".format(id))

    # format:
    response = jsonify(question.to_json())
    return response, 200

#  DELETE
#  ----------------------------------------------------------------
@bp.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    """ DELETE question
    """
    error = True

    try:
        # select:
        question = Question.query.get(id)

        # if resource is not found:
        if question is None:
            abort(404, description="Question with id={} not found".format(id))

        # delete:
        db.session.delete(question)
        db.session.commit()

        error = False
    except:
        # rollback:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500, description="Failed to delete Question with id={}".format(id))
    
    # format:
    response = jsonify(
        {
            "success": True 
        }
    )

    return response, 200

