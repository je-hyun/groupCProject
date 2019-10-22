from app.main import bp
from flask import Flask, render_template, request

from app.models import *
from flask_sqlalchemy import SQLAlchemy
import datetime

'''
@bp.route('/testroute', methods=['GET','POST'])
def testroute():
    users = db.session.query(User).all()
    my_user = db.session.query(User).get(1)


    event = Event(
        id = 3,
        start = datetime.datetime(2018, 6, 3),
        end = datetime.datetime(2018, 6, 4),
        name = "SJU Event",
        price = "30",
        location = "Queens"
    )
    succesfullyAdded = my_user.attend_event(event)
    print(succesfullyAdded)
    return render_template("test.html", users=users)
'''

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("calender.html")

@bp.route('/events_page', methods=['GET', 'POST'])
def events_page():
    events = db.session.query(Event).all()
    return render_template('events_page.html')

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")
