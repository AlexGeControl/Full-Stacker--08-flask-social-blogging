FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ${PWD}/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# defaults to development env.:
ENV FLASK_APP app.py
ENV FLASK_DEBUG true
ENV FLASK_CONFIG development
ENV DEV_DATABASE_URL postgresql://udacity:udacity@db:5432/udasocialbloggingapp
ENV STATIC_PATH /app/application/static