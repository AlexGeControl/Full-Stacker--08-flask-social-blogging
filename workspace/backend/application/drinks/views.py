from application import db
from application.models import Drink

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required

from . import bp

from .forms import DrinkForm

from application.auth.decorators import get_drinks_detail_required, post_drinks_required, patch_drinks_required, delete_drinks_required

#  READ
#  ----------------------------------------------------------------
@bp.route('/', methods=['GET'])
def drinks():
    # data:
    drinks = [
        drink.short() for drink in Drink.query.all()
    ]

    # format:
    drinks=[
        {
            "id": drink["id"],
            "title": drink["title"],
            "recipe": drink["recipe"]
        } for drink in drinks
    ]
    
    return render_template('drinks/pages/drinks.html', drinks=drinks)

@bp.route('/<int:drink_id>')
@login_required
@get_drinks_detail_required
def show_drink(drink_id):
    """ show given drink
    """
    # shows the drink page with given drink_id
    drink = Drink.query.get_or_404(drink_id, description='There is no drink with id={}'.format(drink_id)).long()

    return render_template('drinks/pages/show_drink.html', drink=drink)

#  UPDATE
#  ----------------------------------------------------------------
@bp.route('/<int:drink_id>/edit', methods=['GET', 'POST'])
@login_required
@patch_drinks_required
def edit_drink(drink_id):
    """ render form pre-filled with given drink
    """
    # select drink:
    drink = Drink.query.get_or_404(drink_id, description='There is no drink with id={}'.format(drink_id))

    if request.method == 'GET':
        # init form with selected drink:
        drink = drink.long()
        form = DrinkForm(
            title = drink["title"], 
            recipe = [
                x["name"] for x in drink["recipe"]
            ]
        )
    if request.method == 'POST': 
        # init form with POSTed form:
        form = DrinkForm(request.form)

        if form.validate():        
            try:
                # update drink:
                drink.title = form.title.data
                # insert:
                db.session.add(drink)
                # write
                db.session.commit()
                # on successful registration, flash success
                flash('Drink ' + form.title.data + ' was successfully updated.')
                return redirect(url_for('drinks.drinks'))
            except:
                db.session.rollback()
                # on unsuccessful registration, flash an error instead.
                flash('An error occurred. Drink ' + form.title.data + ' could not be updated.')
            finally:
                db.session.close()
        else:
            # for debugging only:
            flash(form.errors)
            pass
            
    return render_template('drinks/forms/edit_drink.html', form=form, drink=drink)

#  DELETE
#  ----------------------------------------------------------------
@bp.route('/<int:drink_id>', methods=['DELETE'])
@login_required
@delete_drinks_required
def delete_drink(drink_id):
    """ delete drink
    """
    error = True

    try:
        # find:
        drink = Drink.query.get_or_404(drink_id, description='There is no drink with id={}'.format(drink_id))
        drink_name = drink.title
        db.session.delete(drink)
        # write
        db.session.commit()
        # on successful db insert, flash success
        flash('Drink ' + drink_name + ' was successfully deleted!')
        error = False
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Drink could not be deleted.')
        error = True
    finally:
        db.session.close()

    if error:
        abort(400)

    return render_template('pages/home.html')
