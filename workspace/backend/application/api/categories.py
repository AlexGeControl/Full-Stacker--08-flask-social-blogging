from application import db
from application.models import Question, Category

from flask import abort, jsonify

from . import bp


@bp.route('/categories/', methods=['GET'])
def get_categories():
    """ GET all categories as dict with id as key and type as value
    """
    # select all categories:
    categories = {
        _id: _type for (_id, _type) in Category.query.with_entities(
            Category.id,
            Category.type
        ).all()
    }

    # format:
    response = jsonify(
        {"categories": categories}
    )
    
    return response, 200

@bp.route('/categories/<int:id>/questions/', methods=['GET'])
def get_questions_by_category(id):
    """ GET questions by category
    """
    # select category:
    category = Category.query.get(id)

    # if resource is not found:
    if category is None:
        abort(404, description="Category with id={} not found".format(id))

    # select questions:
    questions = Question.query.filter(
        Question.category_id == category.id
    ).all()

    # format:
    response = jsonify(
        {
            "questions": [question.to_json() for question in questions],
            "total_questions": len(questions),
            "current_category": category.id
        }
    )

    return response, 200
