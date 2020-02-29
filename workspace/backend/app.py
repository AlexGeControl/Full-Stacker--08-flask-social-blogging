import os
import sys
import click

from application import create_app, db
from flask_migrate import Migrate

from application.auth.models import Role, User
from application.models import Drink, DrinkFactory

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
Migrate(app, db)

# coverage analysis engine:
cov = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage    
    cov = coverage.coverage(branch=True, include='application/*')    
    cov.start()

@app.shell_context_processor
def make_shell_context():
    # make extra variables available in flask shell context:    
    return dict(db=db, Role=Role, User=User, Drink=Drink)

@app.cli.command()
@click.option(
    '--coverage', default=False,
    help='Run tests under code coverage.'
)
def test(coverage):    
    """ Run the unit tests.
    """    
    # if coverage analysis is needed but the engine is not launched, re-run the command
    if coverage and not os.environ.get('FLASK_COVERAGE'):        
        os.environ['FLASK_COVERAGE'] = 'true'        
        os.execvp(sys.executable, [sys.executable] + sys.argv)    
    
    import unittest    
    
    tests = unittest.TestLoader().discover('tests')    
    unittest.TextTestRunner(verbosity=2).run(tests)    
    
    if cov:
        cov.stop()        
        cov.save()        
        # summary:
        print('Coverage Summary:')        
        cov.report()        
        # detailed report in HTML:
        basedir = os.path.abspath(os.path.dirname(__file__))        
        covdir = os.path.join(basedir, 'coverage')        
        cov.html_report(directory=covdir)        
        print('Detailed report in HTML is available at: file://%s/index.html' % covdir)
        # close:        
        cov.erase()

@app.cli.command()
def init_db():
    """ Pop DB with initial data
    """
    import json
    
    # init db:
    db.drop_all()
    db.create_all()

    # load accounts:
    with open('data/accounts.json') as accounts_json_file:
        accounts = json.load(accounts_json_file)
    
    # add users:
    success = False
    try:
        for user in accounts["users"]:
            db.session.add(User(**user))
        db.session.commit()
        success = True
    except:
        db.session.rollback()
        success=False
    finally:
        db.session.close()

    # load drinks:
    with open('data/drinks.json') as drinks_json_file:
        drinks = json.load(drinks_json_file)
    
    success = False
    try:
        for drink in drinks:
            # serialize recipes as one string:
            drink["recipe"] = json.dumps(drink["recipe"])
            db.session.add(Drink(**drink))
        db.session.commit()
        success = True
    except:
        db.session.rollback()
        success=False
    finally:
        db.session.close()

@app.cli.command()
def list_routes():
    """ List APP routes
    """
    import urllib
    from flask import url_for

    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        output.append(line)

    for line in sorted(output):
        print(line)