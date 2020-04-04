# app>sched>forms.py

from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, BooleanField
from wtforms.fields.html5 import DateField

class AppointmentForm(FlaskForm):
    title = StringField('Title')
    start = DateField('Start')
    end = DateField('End')
    allday = BooleanField('All day')
    location = StringField('Location')
    description = StringField('Description')
    # user_id from the current_user
    submit = SubmitField('Submit')
