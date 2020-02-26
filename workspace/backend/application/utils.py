import os

import dateutil.parser
import babel

import logging
from logging import Formatter, FileHandler


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)

    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"

    return babel.dates.format_datetime(date, format)

def create_file_handler(basedir):
    file_handler = FileHandler(
        os.path.join(basedir, 'error.log')
    )
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    file_handler.setLevel(logging.INFO)

    return file_handler

def convert_form_dict_to_dict(form_dict):
    json = {
        key: (value[0] if len(value) == 1 else value) for key, value in form_dict.to_dict(flat=False).items()
    }

    return json