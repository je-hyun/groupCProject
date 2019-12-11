from flask import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from app.location_utils import coordinatesToAddress, addressToCoordinates
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from app import db



from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from config import Config

#from app import db
#db = SQLAlchemy()

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
    price = db.Column(db.Float)

    location = db.Column(db.String) # TODO: Deprecate this
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    categories = db.relationship('Category', secondary='eventCategory', back_populates="events")
    attending_user = db.relationship('User', secondary='attendEvent', back_populates="events")

    def get_address(self):
        return coordinatesToAddress(self.latitude, self.longitude)

    def conflicts_with_event(self, event):
        return self.start<=event.end and event.start<=self.end

    def save_list_of_categories(self, category_name_list):
        print(category_name_list)
        # Saves categories from a list of strings if the categories already exist on the database
        print("OUT")
        for my_cat in category_name_list:
            my_cat = my_cat.title().strip()
            matching_category = Category.query.filter(Category.name == my_cat).all()
            print(matching_category)
            print("IN")
            if len(matching_category) == 1:
                print("IN IN")
                self.categories.append(matching_category[0])
        db.session.add(self)
        db.session.commit()

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
    preferences = db.relationship('Preference', secondary='preferenceCategory', back_populates="categories")

class PreferenceCategory(db.Model):
    __tablename__ = 'preferenceCategory'
    preference_id = db.Column(db.Integer, db.ForeignKey('preference.preference_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)

'''
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    events = db.relationship('Event', secondary='attendEvent', back_populates="attending_user")
    preference = db.relationship('Preference', uselist=False, backref="user")

    def is_Attending(self, event):
        attending = False;
        userAttendEvent = self.events
        for x in userAttendEvent:
            if x==event:
                attending = True
        return attending

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Float)
    distance = db.Column(db.Integer)

    location = db.Column(db.String) # TODO: Deprecate this
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    size = db.Column(db.String)
    DayFree = db.Column(db.String)
    hoursFree = db.Column(db.String)

#Kamil WorkingForm
    categories = db.relationship('Category', secondary='preferenceCategory', back_populates="preferences")

    def save_list_of_categories(self, category_name_list):
        print(category_name_list)
        # Saves categories from a list of strings if the categories already exist on the database
        print("OUT")
        for my_cat in category_name_list:
            my_cat = my_cat.title().strip()
            matching_category = Category.query.filter(Category.name == my_cat).all()
            print(matching_category)
            print("IN")
            if len(matching_category) == 1:
                print("IN IN")
                self.categories.append(matching_category[0])
        db.session.add(self)
        db.session.commit()

    #def get_address(self):


class TimeSlot(db.Model):
    __tablename__ = 'timeslot'
    timeslot_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

#Kamil Login (databse for users)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', secondary='attendEvent', back_populates="attending_user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
'''

def get_address(self):
    return coordinatesToAddress(self.latitude, self.longitude)

    def distance_preference_conflicts_with_event(self, event):
        if geodesic((self.latitude,self.longitude), (event.latitude,event.longitude)).miles<self.distance:
            return False
        else:
            return True

if __name__ == "__main__":
    Manager.run()
