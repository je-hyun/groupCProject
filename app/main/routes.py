from app.main import bp
from flask import Flask, render_template, request
# from models
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
    # print(event.attending_user)
    for event in events:
        print(event.attending_user)
    return render_template('events_page.html', events=events)

@bp.route('/liked_page', methods=['GET', 'POST'])
def liked_page():
    events = LikedEvent.query.all()
    print(events)
    items = list()
    # 1. Get the user object for the current user (by id)
    current_user_id = 1 # Assume current user id is 1, for testing
    current_user = db.session.query(User).get(current_user_id)
    # 2. Get the event object you want to add
    
    # 3. Add the current event to the liked_events list

    for liked_item in events:
        event_name = Event.query.get(liked_item.id).name
        user_who_liked_event = User.query.get(liked_item.user_id).lastname
        items.append(LikedEventViewModel(event_name, user_who_liked_event))

    return render_template('liked_page.html', events=items)

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")

@bp.route("/like/", methods=['GET', 'POST'])
@bp.route('/add_events', methods=['GET', 'POST'])
def add_events():
    event_form = EventForm()
    if event_form.validate_on_submit():
        event = Event(start=event_form.start.data, end=event_form.end.data, name=event_form.name.data, price=event_form.price.data, location=event_form.location.data)
        db.session.add(event)
        db.session.commit()
        flash('Event Added.')
    return render_template('add_events.html', event_form=event_form)
