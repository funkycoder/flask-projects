# app>misc>forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class DisplayInfoForm(FlaskForm):
    city = StringField('City (temperature)')
    publication = SelectField('Publication (RSS feeds)', choices=[('cnn', 'CNN'),('iol', 'IOL'), ('fox', 'Fox News'), ('vnexpress', 'VN Express'), ('dantri', u'Dân trí')])
    currency_from = SelectField('From currency', default='GBP', coerce=str)
    currency_to = SelectField('To currency', default='USD', coerce=str)
    submit = SubmitField('Update')