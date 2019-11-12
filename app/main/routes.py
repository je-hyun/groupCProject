from app.main import bp
from flask import Flask, render_template, request

from app.models import *
from flask_sqlalchemy import SQLAlchemy
import datetime


@bp.route('/testroute', methods=['GET','POST'])
def testroute():
    users = db.session.query(User).all()
    my_user = db.session.query(User).get(0)

    event = Event(
        id = 0,
        start = datetime.datetime(2018, 8, 1),
        end = datetime.datetime(2018, 8, 2),
        name = "Rock climbing event",
        price = "10",
        location = "NYC"
    )
    succesfullyAdded = db.session.query(User).get(0).attend_event(event)
    succesfullyAdded = db.session.query(User).get(1).attend_event(event)
    succesfullyAdded = db.session.query(User).get(2).attend_event(event)
    print(succesfullyAdded)
    return render_template("test.html", users=users)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("calender.html")

@bp.route('/events_page', methods=['GET', 'POST'])
def events_page():
    events = Event.query.all()
    return render_template('events_page.html', events=events)

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")

@bp.route('/workingtime', methods=['GET', 'POST'])
def add_TimeSlot():
    timeslot_id = request.form.get("timeslot_id")
    day = request.form.get("day")
    startTime = request.form.get("startTime")
    endTime = request.form.get("endTime")
    timeslot = TimeSlot(timeslot_id=timeslot_id, day=day, startTime=startTime, endTime=endTime)
    timeslot = TimeSlot.query.all()
    return render_template("workingtime_form.html")
    #, timeslot=timeslot

'''
def add_course():
    id = request.form.get("id")
    course_number = request.form.get("course_number")
    course_title = request.form.get("course_title")
    
    course = Course(id = id ,course_number=course_number, course_title = course_title)
    db.session.add(course)
    db.session.commit()
    course = Course.query.all()
    return render_template('index.html', course = course)

'''