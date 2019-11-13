import calendar
import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

from app.main import bp
from app.main.forms import EventForm, EventsPageForm
from app.models import *


@bp.route('/testroute', methods=['GET','POST'])
def testroute():
    users = db.session.query(User).all()
    my_user = db.session.query(User).get(0)

    """ event = app.models.Event(
        id = 0,
        start = datetime.datetime(2018, 8, 1),
        end = datetime.datetime(2018, 8, 2),
        name = "Rock climbing event",
        price = "10",
        location = "NYC"
    ) """

    #succesfullyAdded = db.session.query(app.models.User).get(0).attend_event(event)
    #succesfullyAdded = db.session.query(app.models.User).get(1).attend_event(event)
    #succesfullyAdded = db.session.query(app.models.User).get(2).attend_event(event)
    #print(succesfullyAdded)
    return render_template("test.html", users=users)


@bp.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.datetime.now()
    return redirect(url_for('main.calendar_page_monthly', year=now.year, month=now.month))

@bp.route('/calendar_page/monthly/<int:year>/<int:month>/', methods=['GET', 'POST'])
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
    form = EventsPageForm()
    #if form.validate_on_submit():
    if request.method == "POST":
        event_id = request.form.get('event.id')
        event_id = int(event_id)
        attend = AttendEvent(user_id=0, event_id=event_id)
        db.session.add(attend)
        db.session.commit()
        flash('Event added to calendar.')
    events = Event.query.all()
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

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        #return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', login_form=login_form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
