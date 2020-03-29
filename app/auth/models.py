# app>auth>models.py

from app import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True, index=True)
    user_password = db.Column(db.String(80))
    registration_date = db.Column(db.DateTime, default=datetime.now)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)
        
    # Class methods belong to a class but not associated with any class instance
    @classmethod
    def create_user(cls, user, email, password):
        user = cls(user_name=user, user_email=email,
        user_password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return user

    # I haven't seen using this func
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))