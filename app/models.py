from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from app.location_utils import coordinatesToAddress, addressToCoordinates
from app import db

#from app import db
#db = SQLAlchemy()


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
        # Saves categories from a list of strings if the categories already exist on the database
        for my_cat in category_name_list:
            my_cat = my_cat.title().strip()
            matching_category = Category.query.filter(Category.name == my_cat).all()
            if len(matching_category) == 1:
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


    def unattend_event(self, event):
        # checks if event conflicts with any event inside the user's event list
        #   adds event to the user's events list
        hasEvent = False;
        userAttendEvent = self.events
        print(userAttendEvent)
        for x in userAttendEvent:
            if x==event:
                hasEvent = True


        if not hasEvent:
            return False
        else:
            self.events.remove(event)
            db.session.commit()
            return True


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

    categories = db.relationship('Category', secondary='preferenceCategory', back_populates="preferences")

    def save_list_of_categories(self, category_name_list):
        PreferenceCategory.query.filter(PreferenceCategory.preference_id==self.preference_id).delete(synchronize_session=False)
        # Saves categories from a list of strings if the categories already exist on the database
        for my_cat in category_name_list:
            my_cat = my_cat.title().strip()
            matching_category = Category.query.filter(Category.name == my_cat).all()
            if len(matching_category) == 1:
                self.categories.append(matching_category[0])
        db.session.add(self)
        db.session.commit()

    def get_address(self):
        return coordinatesToAddress(self.latitude, self.longitude)

    def distance_preference_conflicts_with_event(self, event):
        if geodesic((self.latitude,self.longitude), (event.latitude,event.longitude)).miles<self.distance:
            return False
        else:
            return True
