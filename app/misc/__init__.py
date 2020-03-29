# app>misc>__init__.py
from flask import Blueprint

misc = Blueprint('misc', __name__, template_folder='templates')
from app.misc import routes