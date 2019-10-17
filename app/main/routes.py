from app.main import bp
from flask import Flask, render_template, request

from app.models import *
from flask_sqlalchemy import SQLAlchemy

@bp.route('/testroute', methods=['GET','POST'])
def testroute():
    users = db.session.query(Users).all()
    return render_template("test.html", users=users)

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
