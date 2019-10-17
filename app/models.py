from flask_sqlalchemy import SQLAlchemy
#from app import db
db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    name = db.Column(db.String)
    price = db.Column(db.String)
    location = db.Column(db.String)
    categories = db.relationship('Category', secondary='eventCategory')
    attending_users = db.relationship('Users', secondary='Attend_Event')
    def conflictsWithEvent(event):
        return start<=event.end and event.start<=end

class EventCategory(db.Model):
    __tablename__ = 'eventCategory'
    event_id = db.Column(
     db.Integer,
     db.ForeignKey('event.id'),
     primary_key=True
    )
    category_id = db.Column(
     db.Integer,
     db.ForeignKey('category.id'),
     primary_key=True
    )

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    events = db.relationship('Event', secondary='eventCategory')

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    events = db.relationship('Event', secondary='Attend_Event')

class Attend_Event(db.Model):
    __tablename__ = 'Attend_Event'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

class Preference(db.Model):
    __tablename__ = 'preference'
    preference_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    location = db.Column(db.String)
    size = db.Column(db.String)
    DayFree = db.relationship(db.String)
    hoursFree = db.relationship(db.String)
