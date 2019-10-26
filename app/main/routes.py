from app.main import bp
from flask import Flask, render_template, request
import calendar

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

    c = calendar.TextCalendar(calendar.SUNDAY)

    daylist = list(c.itermonthdays(2019, 10))
    return render_template("calender.html", daylist=daylist)

@bp.route('/events_page', methods=['GET', 'POST'])
def events_page():
    events = Event.query.all()
    return render_template('events_page.html', events=events)

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")
