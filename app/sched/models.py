# app>book>models.py
from app import db
from datetime import datetime


class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    allday = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    # Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # __init__ is called when new instances are created
    def __init__(self,
                 title,
                 start,
                 end,
                 allday,
                 location,
                 description,
                 user_id):
        self.title = title
        self.start = start
        self.end = end
        self.allday = allday
        self.location = location
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return 'Appointment: {} |start: {} | end:{} | location: {} | created: {} | last modified: {}'.format(self.title, self.start, self.end, self.location, self.created, self.modified)


@property
def duration(self):
    delta = self.end - self.start
    return delta.days * 24 * 60 * 60 + delta.seconds
