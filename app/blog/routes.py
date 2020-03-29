# app>blog>routes.py
from app.blog import main
from flask import render_template
# The last route will be used for url_for return address
@main.route('/index')
@main.route('/blog')
@main.route('/')
def index():
    return render_template('home.html')

