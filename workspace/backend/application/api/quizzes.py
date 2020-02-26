import random

from application import db
from application.models import Question, Category

from flask import current_app
from flask import request, abort, jsonify

from . import bp


#  READ
#  ----------------------------------------------------------------
@bp.route('/quizzes/', methods=['POST'])
def get_quizzes():
    """ GET all questions including pagination
    """
    # parse previous questions:
    previous_questions = request.get_json().get("previous_questions", None)
    
    if previous_questions is None:
        abort(400, description="'previous_questions' not found")

    # parse quiz category:
    quiz_category = request.get_json().get("quiz_category", None)
    
    # extract questions:
    questions = []
    if quiz_category is None or quiz_category["id"] == 0:
        questions = Question.query.filter(
            Question.id.notin_(previous_questions) 
        ).all()
    else:
        questions = Question.query.filter(
            Question.id.notin_(previous_questions) 
        ).filter(
            Question.category_id == quiz_category["id"]
        ).all()

    # format:
    response = {
        "question": None
    }
    if len(questions):
        # if there are still remaining questions, select one randomly from them
        response["question"] = random.choice(questions).to_json()

    response = jsonify(response)
    return response, 200
