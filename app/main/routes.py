from app.main import bp
from flask import Flask, render_template, request, flash, redirect, url_for
import calendar
from app.main.forms import EventForm, EventsPageForm
from app.models import *
from app import db
from flask_sqlalchemy import SQLAlchemy
import datetime


@bp.route('/testroute', methods=['GET','POST'])
def testroute():
    users = db.session.query(User).all()
    my_user = db.session.query(User).get(0)

    """ event = Event(
        id = 0,
        start = datetime.datetime(2018, 8, 1),
        end = datetime.datetime(2018, 8, 2),
        name = "Rock climbing event",
        price = "10",
        location = "NYC"
    ) """

    #succesfullyAdded = db.session.query(User).get(0).attend_event(event)
    #succesfullyAdded = db.session.query(User).get(1).attend_event(event)
    #succesfullyAdded = db.session.query(User).get(2).attend_event(event)
    #print(succesfullyAdded)
    return render_template("test.html", map_lat=0.0, map_lon=0.0)


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

@bp.route('/calendar_page/weekly/<int:year>/<int:month>/<int:week>')
def calendar_page_weekly(year, month, week):
    if (month > 12 or month < 1):
        return ("Oops, the month is out of range!")
    # Initialize some useful variables:
    current_user_id = 0
    c = calendar.TextCalendar(calendar.SUNDAY) # Calendar object starting on Sunday
    now = datetime.datetime.now()
    event_list = Event.query.all()
    month_name = calendar.month_name[month]
    daylist = list(c.itermonthdays(year, month))
    day_delta = datetime.timedelta(days=1)
    # daylist is the list of numbers to put in each box of the calendar,
    # where 0 is an empty box, and 1 is the 1st of the month, etc.
    # example: [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 0, 0]
    if len(daylist) <= (week-1) * 7 or week < 1:
        return ("Oops, the week is out of range!")

    if (month == 1):
        days_in_previous_month = len(list(c.itermonthdays(year-1,12)))
    else:
        days_in_previous_month = len(list(c.itermonthdays(year,month-1)))

    event_list = [None] * len(daylist)

    week_of_today = (daylist.index(now.day) // 7) + 1
    # The following loop creates an event_list with event objects inside
    # The indices correspond with the indices in daylist
    for day_index in range(len(daylist)):
        if daylist[day_index] != 0:
            day = datetime.datetime(year, month, daylist[day_index])
            event_list[day_index] = Event.query.filter(Event.start >= day, Event.start < day+day_delta, Event.attending_user.any(User.id==current_user_id)).all()
    return render_template("calender_week.html", now=now, month_name=month_name, month=month, year=year, daylist=daylist, event_list=event_list, week=week, days_in_previous_month=days_in_previous_month, week_of_today=week_of_today)


@bp.route('/calendar_page/daily/<int:year>/<int:month>/<int:currentDay>')
def calendar_page_daily(year, month, currentDay):
    if (month > 12 or month < 1):
        return ("Oops, the month is out of range!")
    # Initialize some useful variables:
    current_user_id = 0
    c = calendar.TextCalendar(calendar.SUNDAY) # Calendar object starting on Sunday
    now = datetime.datetime.now()
    event_list = Event.query.all()
    month_name = calendar.month_name[month]
    daylist = list(c.itermonthdays(year, month))
    day_delta = datetime.timedelta(days=1)
    # daylist is the list of numbers to put in each box of the calendar,
    # where 0 is an empty box, and 1 is the 1st of the month, etc.
    # example: [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 0, 0]

    if (month == 1):
        days_in_previous_month = calendar.monthrange(year-1, 12)[1]
    else:
        days_in_previous_month = calendar.monthrange(year, month-1)[1]

    days_in_current_month = calendar.monthrange(year, month)[1]

    event_list = [None]

    # The following loop creates an event_list with event objects inside
    # The indices correspond with the indices in daylist
    day = datetime.datetime(year, month, currentDay)
    event_list[0] = Event.query.filter(Event.start >= day, Event.start < day+day_delta, Event.attending_user.any(User.id==current_user_id)).all()
    return render_template("calender_day.html", now=now, month_name=month_name, month=month, year=year, daylist=daylist, event_list=event_list, currentDay=currentDay, days_in_previous_month=days_in_previous_month, days_in_current_month=days_in_current_month)








@bp.route('/events_page/<int:sortby>/', methods=['GET', 'POST'])
def events_page(sortby):
    #sortby can be [0,1,2,3,4], representing sorting by:
    #ID/Start Time/Name/Price/Location Respectively
    form = EventsPageForm()
    if form.validate_on_submit():
        event_id = request.form['event.id']
        attend = AttendEvent(user_id=0, event_id=event_id)
        flash('Test')
    if sortby==0:
        events = Event.query.order_by(Event.id)
    elif sortby==1:
        events = Event.query.order_by(Event.start)
    elif sortby==2:
        events = Event.query.order_by(Event.name)
    elif sortby==3:
        events = Event.query.order_by(Event.price)
    elif sortby==4:
        events = Event.query.order_by(Event.location)
    else:
        events = Event.query.order_by(Event.id)

    return render_template('events_page.html', events=events, form=form)

@bp.route('/add_events', methods=['GET', 'POST'])
def add_events():
    event_form = EventForm()
    if event_form.validate_on_submit():
        event = Event(start=event_form.start.data, end=event_form.end.data, name=event_form.name.data, price=event_form.price.data, location=event_form.location.data)
        db.session.add(event)
        db.session.commit()
        flash('Event Added.')
    return render_template('add_events.html', event_form=event_form)

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")

@bp.route('/save_preference', methods=['POST'])
def save_preference():
    return render_template("save_preference.html")

@bp.route('/event/<int:id>', methods=['GET', 'POST'])
def event(id):
    form = EventsPageForm()

    if form.validate_on_submit():
        event_id = request.form['event.id']
        attend = AttendEvent(user_id=id, event_id=event_id)
        flash('Test')

    a = [Event.query.get(id)]
    return render_template('single_event_page.html', events=a, form=form)
