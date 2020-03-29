# run.py

# from the app package __init__.py
from app import create_app, db  
# from app.auth.models import User

# My home page is at blog component
if __name__ == '__main__':
    flask_app = create_app('dev')
    with flask_app.app_context():
        db.create_all()
    flask_app.run()