from flask import Blueprint

appointment = Blueprint('appointment', __name__, template_folder='templates')
from app.sched import routes  # to avoid circular imports
