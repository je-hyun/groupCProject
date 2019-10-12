from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
'''
Reference database m:n (TODO: delete after)
class RegisteredStudent(db.Model):
    __tablename__ = 'registeredstudent'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    grade = db.Column(db.Integer)
    courses = db.relationship('Course', secondary='link')


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String)
    course_title = db.Column(db.String)
    students = db.relationship('RegisteredStudent', secondary='link')

class Link(db.Model):
   __tablename__ = 'link'
   registeredstudent_id = db.Column(
      db.Integer,
      db.ForeignKey('registeredstudent.id'),
      primary_key=True)

   course_id = db.Column(
       db.Integer,
       db.ForeignKey('course.id'),
       primary_key=True)

'''

'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categories = db.relationship('Event', secondary='userSchedule')
    username = db.Column(db.String)
    schedule = db.relationship('Event', secondary='schedule')

class UserSchedule(db.Model):
    __tablename__ = 'userSchedule'

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('event.id'),
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True
    )
'''

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    name = db.Column(db.String)
    price = db.Column(db.String)
    location = db.Column(db.String)
    categories = db.relationship('Category', secondary='eventCategory')

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