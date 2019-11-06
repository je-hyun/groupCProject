
from app.main import bp
from flask import Flask, render_template, request, redirect
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
    events = Event.query.all()
    return render_template('liked_page.html', events=events)

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")

@bp.route('/add_like/<int:event_id>', methods=['GET', 'POST'])
def add_like(event_id):
    current_user_id = 0
    event = Event.query.get(event_id)
    user = User.query.get(current_user_id)
    event.liked_user.append(user)
    db.session.add(event)
    db.session.add(user)
    db.session.commit()
    # add user in likedEvent
    return redirect("/liked_page")
