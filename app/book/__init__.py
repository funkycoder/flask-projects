from flask import Blueprint

book = Blueprint('book', __name__, template_folder='templates')
from app.book import routes  # to avoid circular imports
