#!/bin/bash

# create app
# heroku create d-and-g-uda-social-blogging
# show heroku git repo:
git remote show heroku

# set up env vars in heroku
heroku config:set FLASK_APP=app.py
heroku config:set FLASK_CONFIG=heroku
heroku config:set STATIC_PATH=/app/application/static
heroku config:set AUTH0_MANAGEMENT_TOKEN=${AUTH0_MANAGEMENT_TOKEN}
heroku config:set AUTH0_CLIENT_SECRET=${AUTH0_CLIENT_SECRET}

# create PG SQL instance:
heroku addons:create heroku-postgresql:hobby-dev