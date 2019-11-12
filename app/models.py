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
    categories = db.relationship('Category', secondary='eventCategory', back_populates="events")
    attending_user = db.relationship('User', secondary='attendEvent', back_populates="events")
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


class AttendEvent(db.Model):
    __tablename__ = 'attendEvent'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

class Preference(db.Model):
    __tablename__ = 'preference'
    preference_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    location = db.Column(db.String)
    size = db.Column(db.String)
    DayFree = db.Column(db.String)
    hoursFree = db.Column(db.String)

class TimeSlot(db.Model):
    __tablename__ = 'timeslot'
    timeslot_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
