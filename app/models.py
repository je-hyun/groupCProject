from flask import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim
from app.location_utils import coordinatesToAddress, addressToCoordinates
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from config import Config
#bootstrap = Bootstrap(app)


db = SQLAlchemy()
migrate = Migrate(app, db)


#login_manager = LoginManager()
#login_manager.login_view = 'login'
#login_manager.init_app(app)

#Manager.add_command('db', MigrateCommand)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    name = db.Column(db.String)
    price = db.Column(db.String)

    location = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    categories = db.relationship('Category', secondary='eventCategory', back_populates="events")
    attending_user = db.relationship('User', secondary='attendEvent', back_populates="events")

    def get_address(self):
        return coordinatesToAddress(self.latitude, self.longitude)

    def conflicts_with_event(self, event):
        return self.start<=event.end and event.start<=self.end

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
    events = db.relationship('Event', secondary='eventCategory', back_populates="categories")

'''
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    events = db.relationship('Event', secondary='attendEvent', back_populates="attending_user")
    def attend_event(self, event):
        # checks if event conflicts with any event inside the user's event list
        #   adds event to the user's events list
        conflicts = False;
        userAttendEvent = self.events
        print(userAttendEvent)
        for x in userAttendEvent:
            if x.conflicts_with_event(event):
                conflicts = True
        if conflicts:
            return False
        else:
            self.events.append(event)
            db.session.add(event)
            db.session.add(self)
            db.session.commit()
            return True

'''

class AttendEvent(db.Model):
    __tablename__ = 'attendEvent'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

class Preference(db.Model):
    __tablename__ = 'preference'
    preference_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)

    location = db.Column(db.String) # TODO: Deprecate this
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    size = db.Column(db.String)
    DayFree = db.Column(db.String)
    hoursFree = db.Column(db.String)

#Kamil WorkingForm
class TimeSlot(db.Model):
    __tablename__ = 'timeslot'
    timeslot_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)

#Kamil Login (databse for users)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), index=True, unique=True)
    email = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(60))
    events = db.relationship('Event', secondary='attendEvent', back_populates="attending_user")

'''

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
'''

    def __repr__(self):
        return '<User {}>'.format(self.username)


def get_address(self):
        return coordinatesToAddress(self.latitude, self.longitude)

if __name__ == "__main__":
    Manager.run()
