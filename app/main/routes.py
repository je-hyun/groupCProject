from app.main import bp
from flask import Flask, render_template, request, flash
from app.main.forms import EventForm, EventsPageForm

from app.models import *
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
    return render_template("test.html", users=users)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("calender.html")

@bp.route('/events_page', methods=['GET', 'POST'])
def events_page():
    form = EventsPageForm()
    if form.validate_on_submit():
        event_id = request.form['event.id']
        attend = AttendEvent(user_id=0, event_id=event_id)
        flash('Test')
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
