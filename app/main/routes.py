from app.main import bp
from flask import Flask, render_template, request, redirect, url_for
import calendar

from app.models import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import datetime
from sqlalchemy import func


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
    now = datetime.datetime.now()
    return redirect(url_for('main.calendar_page_monthly', year=now.year, month=now.month))

@bp.route('/calendar_page/monthly/<int:year>/<int:month>/')
def calendar_page_monthly(year, month):

    if (month > 12 or month < 1):
        return ("Oops, the month is out of range!")
    # Initialize some useful variables:
    current_user_id = 0
    c = calendar.TextCalendar(calendar.SUNDAY) # Calendar object starting on Sunday
    now = datetime.datetime.now()
    event_list = Event.query.all()
    month_name = calendar.month_name[month]
    daylist = list(c.itermonthdays(year, month))
    print("daylist = ",daylist, "length", len(daylist))
    day_delta = datetime.timedelta(days=1)
    # daylist is the list of numbers to put in each box of the calendar,
    # where 0 is an empty box, and 1 is the 1st of the month, etc.
    # example: [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 0, 0]

    event_list = [None] * len(daylist)
    # The following loop creates an event_list with event objects inside
    # The indices correspond with the indices in daylist
    for day_index in range(len(daylist)):
        if daylist[day_index] != 0:
            day = datetime.datetime(year, month, daylist[day_index])
            event_list[day_index] = Event.query.filter(Event.start >= day, Event.start < day+day_delta, Event.attending_user.any(User.id==current_user_id)).all()
    return render_template("calender.html", now=now, month_name=month_name, month=month, year=year, daylist=daylist, event_list=event_list)


@bp.route('/events_page', methods=['GET', 'POST'])
def events_page():
    events = Event.query.all()
    return render_template('events_page.html', events=events)

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")

@bp.route('/save_preference', methods=['POST'])
def save_preference():
    return render_template("save_preference.html")
